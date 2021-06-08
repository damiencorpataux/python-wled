"""Models for WLED."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .exceptions import WLEDError


@dataclass
class Nightlight:
    """Object holding nightlight state in WLED."""

    duration: int
    fade: bool
    on: bool
    target_brightness: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Nightlight:
        """Return Nightlight object from WLED API response.

        Args:
            data: The data from the WLED device API.

        Returns:
            A Nightlight object.
        """
        nightlight = data.get("nl", {})
        return Nightlight(
            duration=nightlight.get("dur", 1),
            fade=nightlight.get("fade", False),
            on=nightlight.get("on", False),
            target_brightness=nightlight.get("tbri", 0),
        )


@dataclass
class Sync:
    """Object holding sync state in WLED."""

    receive: bool
    send: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Sync:
        """Return Sync object from WLED API response.

        Args:
            data: The data from the WLED device API.

        Returns:
            A sync object.
        """
        sync = data.get("udpn", {})
        return Sync(send=sync.get("send", False), receive=sync.get("recv", False))


@dataclass
class Effect:
    """Object holding an effect in WLED."""

    effect_id: int
    name: str


@dataclass
class Palette:
    """Object holding an palette in WLED.

    Args:
        data: The data from the WLED device API.

    Returns:
        A palette object.
    """

    name: str
    palette_id: int


@dataclass
class Segment:
    """Object holding segment state in WLED.

    Args:
        data: The data from the WLED device API.

    Returns:
        A segment object.
    """

    brightness: int
    clones: int
    color_primary: tuple[int, int, int, int] | tuple[int, int, int]
    color_secondary: tuple[int, int, int, int] | tuple[int, int, int]
    color_tertiary: tuple[int, int, int, int] | tuple[int, int, int]
    effect: Effect
    intensity: int
    length: int
    on: bool
    palette: Palette
    reverse: bool
    segment_id: int
    selected: bool
    speed: int
    start: int
    stop: int

    @staticmethod
    def from_dict(
        segment_id: int,
        data: dict[str, Any],
        *,
        effects: list[Effect],
        palettes: list[Palette],
        state_on: bool,
        state_brightness: int,
    ) -> Segment:
        """Return Segment object from WLED API response.

        Args:
            segment_id: The ID of the LED strip segment.
            data: The segment data received from the WLED device.
            effects: A list of Effect objects.
            palettes: A list of Palette objects.
            state_on: Boolean the represents the on/off state of this segment.
            state_brightness: The brightness level of this segment.

        Returns:
            An Segment object.
        """
        start = data.get("start", 0)
        stop = data.get("stop", 0)
        length = data.get("len", (stop - start))

        colors = data.get("col", [])
        primary_color, secondary_color, tertiary_color = (0, 0, 0)
        try:
            primary_color = tuple(colors.pop(0))  # type: ignore
            secondary_color = tuple(colors.pop(0))  # type: ignore
            tertiary_color = tuple(colors.pop(0))  # type: ignore
        except IndexError:
            pass

        effect = next(
            (item for item in effects if item.effect_id == data.get("fx", 0)),
            Effect(effect_id=0, name="Unknown"),
        )
        palette = next(
            (item for item in palettes if item.palette_id == data.get("pal", 0)),
            Palette(palette_id=0, name="Unknown"),
        )

        return Segment(
            brightness=data.get("bri", state_brightness),
            clones=data.get("cln", -1),
            color_primary=primary_color,  # type: ignore
            color_secondary=secondary_color,  # type: ignore
            color_tertiary=tertiary_color,  # type: ignore
            effect=effect,
            intensity=data.get("ix", 0),
            length=length,
            on=data.get("on", state_on),
            palette=palette,
            reverse=data.get("reverse", False),
            segment_id=segment_id,
            selected=data.get("sel", False),
            speed=data.get("sx", 0),
            start=start,
            stop=stop,
        )


@dataclass
class Leds:
    """Object holding leds info from WLED."""

    count: int
    fps: int | None
    max_power: int
    max_segments: int
    pin: int
    power: int
    rgbw: bool
    wv: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Leds:
        """Return Leds object from WLED API response.

        Args:
            data: The data from the WLED device API.

        Returns:
            A Leds object.
        """
        leds = data.get("leds", {})
        return Leds(
            count=leds.get("count", 0),
            fps=leds.get("fps", None),
            max_power=leds.get("maxpwr", 0),
            max_segments=leds.get("maxseg", 0),
            pin=leds.get("pin", 0),
            power=leds.get("pwr", 0),
            rgbw=leds.get("rgbw", False),
            wv=leds.get("wv", True),
        )


@dataclass
class Wifi:
    """Object holding Wi-Fi information from WLED.

    Args:
        data: The data from the WLED device API.

    Returns:
        A Wi-Fi object.
    """

    bssid: str
    channel: int
    rssi: int
    signal: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Wifi | None:
        """Return Wifi object form WLED API response.

        Args:
            data: The response from the WLED API.

        Returns:
            An Wifi object.
        """
        if "wifi" not in data:
            return None
        wifi = data.get("wifi", {})
        return Wifi(
            bssid=wifi.get("bssid", "00:00:00:00:00:00"),
            channel=wifi.get("channel", 0),
            rssi=wifi.get("rssi", 0),
            signal=wifi.get("signal", 0),
        )


@dataclass
class Info:
    """Object holding information from WLED."""

    architecture: str
    arduino_core_version: str
    brand: str
    build_type: str
    effect_count: int
    free_heap: int
    leds: Leds
    live_ip: str
    live_mode: str
    live: bool
    mac_address: str
    name: str
    pallet_count: int
    product: str
    udp_port: int
    uptime: int
    version_id: str
    version: str
    websocket: int | None
    wifi: Wifi | None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Info:
        """Return Info object from WLED API response.

        Args:
            data: The data from the WLED device API.

        Returns:
            A info object.
        """
        websocket = data.get("ws")
        if websocket == -1:
            websocket = None

        return Info(
            architecture=data.get("arch", "Unknown"),
            arduino_core_version=data.get("core", "Unknown").replace("_", "."),
            brand=data.get("brand", "WLED"),
            build_type=data.get("btype", "Unknown"),
            effect_count=data.get("fxcount", 0),
            free_heap=data.get("freeheap", 0),
            leds=Leds.from_dict(data),
            live_ip=data.get("lip", "Unknown"),
            live_mode=data.get("lm", "Unknown"),
            live=data.get("live", False),
            mac_address=data.get("mac", ""),
            name=data.get("name", "WLED Light"),
            pallet_count=data.get("palcount", 0),
            product=data.get("product", "DIY Light"),
            udp_port=data.get("udpport", 0),
            uptime=data.get("uptime", 0),
            version_id=data.get("vid", "Unknown"),
            version=data.get("ver", "Unknown"),
            websocket=websocket,
            wifi=Wifi.from_dict(data),
        )


@dataclass
class State:
    """Object holding the state of WLED."""

    brightness: int
    nightlight: Nightlight
    on: bool
    playlist: int
    preset: int
    segments: list[Segment]
    sync: Sync
    transition: int

    @property
    def playlist_active(self) -> bool:
        """Return if a playlist is currently active.

        Returns:
            True if there is currently a playlist active, False otherwise.
        """
        return self.playlist == -1

    @property
    def preset_active(self) -> bool:
        """Return if a preset is currently active.

        Returns:
            True is a preset is currently active, False otherwise.
        """
        return self.preset == -1

    @staticmethod
    def from_dict(
        data: dict[str, Any], effects: list[Effect], palettes: list[Palette]
    ) -> State:
        """Return State object from WLED API response.

        Args:
            data: The state response received from the WLED device API.
            effects: A list of effect objects.
            palettes: A list of palette object.

        Returns:
            A State object.
        """
        brightness = data.get("bri", 1)
        on = data.get("on", False)

        segments = [
            Segment.from_dict(
                segment_id=segment_id,
                data=segment,
                effects=effects,
                palettes=palettes,
                state_on=on,
                state_brightness=brightness,
            )
            for segment_id, segment in enumerate(data.get("seg", []))
        ]

        return State(
            brightness=brightness,
            nightlight=Nightlight.from_dict(data),
            on=on,
            playlist=data.get("pl", -1),
            preset=data.get("ps", -1),
            segments=segments,
            sync=Sync.from_dict(data),
            transition=data.get("transition", 0),
        )


class Device:
    """Object holding all information of WLED."""

    effects: list[Effect] = []
    info: Info
    palettes: list[Palette] = []
    state: State

    def __init__(self, data: dict) -> None:
        """Initialize an empty WLED device class.

        Args:
            data: The full API response from a WLED device.

        Raises:
            WLEDError: In case the given API response is incomplete in a way
                that a Device object cannot be constructed from it.
        """
        # Check if all elements are in the passed dict, else raise an Error
        if any(
            k not in data and data[k] is not None
            for k in ["effects", "palettes", "info", "state"]
        ):
            raise WLEDError("WLED data is incomplete, cannot construct device object")
        self.update_from_dict(data)

    def update_from_dict(self, data: dict) -> Device:
        """Return Device object from WLED API response.

        Args:
            data: Update the device object with the data received from a
                WLED device API.

        Returns:
            The updated Device object.
        """
        if _effects := data.get("effects"):
            effects = [
                Effect(effect_id=effect_id, name=effect)
                for effect_id, effect in enumerate(_effects)
            ]
            effects.sort(key=lambda x: x.name)
            self.effects = effects

        if _palettes := data.get("palettes"):
            palettes = [
                Palette(palette_id=palette_id, name=palette)
                for palette_id, palette in enumerate(_palettes)
            ]
            palettes.sort(key=lambda x: x.name)
            self.palettes = palettes

        if _info := data.get("info"):
            self.info = Info.from_dict(_info)

        if _state := data.get("state"):
            self.state = State.from_dict(_state, self.effects, self.palettes)

        return self
