# NetLogo 7 File Format

NetLogo 7 uses `.nlogox` files, which are XML documents (not the old plain-text `.nlogo` format).

## Basic Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<model version="NetLogo 7.0.3" snapToGrid="false">
  <code>...</code>
  <widgets>...</widgets>
  <info><![CDATA[...]]></info>
</model>
```

## Sections

### `<code>`

Contains the NetLogo code (procedures, globals, etc.). XML entities must be escaped:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`

### `<widgets>`

Defines the Interface tab elements. Common widgets:

**View (the main world display):**
```xml
<view x="210" y="10" width="700" height="500"
      minPxcor="0" maxPxcor="268" minPycor="0" maxPycor="158"
      patchSize="1.0" fontSize="10" frameRate="30.0"
      wrappingAllowedX="false" wrappingAllowedY="false"
      showTickCounter="true" tickCounterLabel="ticks"
      updateMode="1"></view>
```

- `minPxcor/maxPxcor/minPycor/maxPycor` — world dimensions in patches
- `patchSize` — pixels per patch
- `wrappingAllowedX/Y` — whether world wraps (toroidal)
- `updateMode` — 0=continuous, 1=on ticks

**Button:**
```xml
<button x="20" y="20" width="80" height="40"
        display="Setup"
        forever="false"
        disableUntilTicks="false"
        kind="Observer">setup</button>
```

- `display` — button label
- `forever` — true for "forever" buttons (like `go`)
- `disableUntilTicks` — grays out until ticks start
- `kind` — "Observer", "Turtle", "Patch", or "Link"
- Text content is the command to run

**Slider:**
```xml
<slider x="20" y="100" width="180" height="50"
        display="population"
        variable="population"
        min="0.0" max="1000.0" default="100.0" step="1.0"
        direction="Horizontal"></slider>
```

- `direction` — must be capitalized: `"Horizontal"` or `"Vertical"`
- `min/max/default/step` — use floats (e.g., `100.0` not `100`)
- The slider automatically creates the variable — do NOT also declare it in `globals`

**Monitor:**
```xml
<monitor x="20" y="160" width="100" height="40"
         display="Count"
         precision="0"
         fontSize="11">count turtles</monitor>
```

**Output (text console):**
```xml
<output x="20" y="200" width="180" height="150" fontSize="11"></output>
```

**Plot:**
```xml
<plot x="20" y="300" width="200" height="150"
      display="Population"
      xAxis="Time" yAxis="Count"
      xMin="0.0" xMax="100.0" yMin="0.0" yMax="100.0"
      autoPlotX="true" autoPlotY="true"
      legend="true">
  <setup></setup>
  <update></update>
  <pen interval="1.0" mode="0" display="turtles" color="-2674135" legend="true">
    <setup></setup>
    <update>plot count turtles</update>
  </pen>
</plot>
```

### `<info>`

The Info tab content in Markdown format, wrapped in `<![CDATA[...]]>`.

## Example: Minimal Model

```xml
<?xml version="1.0" encoding="utf-8"?>
<model version="NetLogo 7.0.3" snapToGrid="false">
  <code>to setup
  clear-all
  create-turtles 100 [
    setxy random-xcor random-ycor
  ]
  reset-ticks
end

to go
  ask turtles [ fd 1 rt random 30 - 15 ]
  tick
end</code>
  <widgets>
    <view x="210" y="10" width="400" height="400"
          minPxcor="-16" maxPxcor="16" minPycor="-16" maxPycor="16"
          patchSize="12.0" fontSize="10" frameRate="30.0"
          wrappingAllowedX="true" wrappingAllowedY="true"
          showTickCounter="true" tickCounterLabel="ticks"
          updateMode="1"></view>
    <button x="20" y="20" width="80" height="40"
            display="Setup" forever="false"
            disableUntilTicks="false" kind="Observer">setup</button>
    <button x="110" y="20" width="80" height="40"
            display="Go" forever="true"
            disableUntilTicks="true" kind="Observer">go</button>
  </widgets>
  <info><![CDATA[## My Model

A simple random walk model.
]]></info>
</model>
```

## GIS Extension Notes

The GIS extension is bundled with NetLogo 7 (in `extensions/.bundled/gis/`).

### Supported Formats

- **Rasters:** ESRI ASCII Grid only (`.asc` or `.grd`). GeoTIFF is NOT supported.
- **Vectors:** ESRI Shapefile (`.shp`), GeoJSON (`.geojson`)

### Supported Projections

NetLogo's GIS extension only supports certain projection types. **EPSG:2913 (Oregon State Plane) is NOT supported** — it uses `Lambert_Conformal_Conic` but NetLogo wants `Lambert_Conformal_Conic_2SP`.

**Supported projections include:**
- Transverse_Mercator (UTM zones) ← **use this**
- Lambert_Conformal_Conic_2SP
- Albers_Conic_Equal_Area
- Mercator_1SP
- And others (see NetLogo GIS extension docs)

**For this project:** Keep EPSG:2913 as the canonical CRS for analysis, but convert to UTM Zone 10N (EPSG:26910) for NetLogo.

### Converting Data for NetLogo

```bash
# Reproject to UTM and convert to ASCII Grid
gdalwarp -t_srs EPSG:26910 -tr 1 1 -r bilinear input.tif output_utm.tif
gdal_translate -of AAIGrid output_utm.tif output_utm.asc
```

### Basic Usage

```netlogo
extensions [gis]

globals [elevation-data]

patches-own [elevation]

to setup
  set elevation-data gis:load-dataset "/absolute/path/to/file.asc"
  gis:set-world-envelope gis:envelope-of elevation-data
  gis:apply-raster elevation-data elevation
end
```

## Gotchas and Lessons Learned

### Variables from widgets
Sliders, choosers, and switches automatically create their variables. If you also declare them in `globals`, you'll get "There is already a variable called X" error.

### Agent references default to 0
Patch variables that store agent references (like `flow-to` for D8 routing) default to `0`, not `nobody`. Use `is-patch?` to check validity:
```netlogo
; Wrong - will fail if flow-to is 0
ask patches with [flow-to != nobody] [ ... ]

; Right
ask patches with [is-patch? flow-to] [ ... ]
```

### XML escaping in code
The `<code>` section is XML, so comparison operators must be escaped:
- `<` → `&lt;`
- `>` → `&gt;`
- `<=` → `&lt;=`
- `>=` → `&gt;=`

### Breeds
Declare breeds before globals:
```netlogo
breed [waters water]

globals [ ... ]
```

### Absolute paths
The GIS extension requires absolute paths to data files. Relative paths from the model location don't work reliably.
