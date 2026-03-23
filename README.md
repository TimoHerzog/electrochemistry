# Electrochemistry
Simple functions for processing electrochemical lab data

# General
- EChem follows an object-oriented approach: Every measurement you import is an instance of one of the classes defined below, e.g. `CV`, `CP` etc. All operations that you can perform on a measurement are methods of these classes.
- All physical units are assumed to be in basic SI units without prefixes, ie Volt, Ampere, Ohm etc.

# `CV` class
Represents a single cycle of a Cyclic Voltammetry (CV) scan.
## Instancing
The `CV` object gets instanced by importing data from an external file. Multiple function for the file formats of different potentiostat manufacturers are available.
Of course, it can also be manually instanced by calling the class:
`myCVInstance = CV([0.1, 0.15, 0.2], [0.03, 0.05, 0.02])`

| Argument | Type           | Description                                            |
| :------: | -------------- | ------------------------------------------------------ |
| `volts`  | `Array: float` | Voltage measurement points of the CV cycle in volts.   |
|  `amps`  | `Array: float` | Current measurement points of the CV cycle in amperes. |

## Methods
### `CV.getPotentialAt`
Returns the nearest current value to the potential value provided. Throws an exception if the nearest potential point is farther away than specified with `maxCurrentDistance`.
Returns a `float`.

|     Argument     | Type  | Default value | Description                                                 |
| :--------------: | ----- | ------------- | ----------------------------------------------------------- |
|    `current`     | float | *none*        | Current in amperes to get the potential value at.           |
| `maxCurrentDist` | float | `0.01`        | Maximum allowed difference before an exception gets thrown. |

### `CV.getCurrentAt`
Analogue to `CV.getPotentialAt`

### `CV.shiftPotential`
|   Argument   | Type  | Default value | Description                          |
| :----------: | ----- | ------------- | ------------------------------------ |
| `shiftVolts` | float | *none*        | Voltage in volts to shift the CV by. |
Adds `shiftVolts` to all voltage values in the CV.
Returns a `CV` object with the shifted volts.

### `CV.beforeRightVertex`, `CV.afterRightVertex`, `CV.beforeLeftVertex`, `CV.afterLeftVertex()`
Return a CV object with a subset of the input data split a vertex as specified, including the vertex.

### `CV.iRCompensate(resistance)`

Applies $iR$ compensation to all voltage points in a CV scan by applying the formula with the provided resistance $R$:

$U_{\mathrm{output},i} = U_{\mathrm{input},i} - I_{\mathrm{input},i} \cdot R$

|   Argument   | Type  | Default value | Description                          |
| :----------: | ----- | ------------- | ------------------------------------ |
| `resistance` | float | *none*        | Ohmic drop $R$ to compensate for. |