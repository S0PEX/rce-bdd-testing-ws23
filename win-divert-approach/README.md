# WinDivert Integration for RCE Network Testing

This directory contains all the necessary components and instructions for integrating WinDivert-based network testing into the RCE (Remote Component Environment) application. Our approach utilizes WinDivert to simulate network conditions and test the resilience and functionality of the RCE under various network scenarios.

## Prerequisites

Before you begin, you need to include the WinDivert Java binding, jDivert, for example from the [mvn repo](https://mvnrepository.com/artifact/com.github.ffalcinelli/jdivert), into the RCE project. This binding is crucial for interfacing Java code with the WinDivert library.

## Structure

This repository is organized as follows:

- **rce directory**: This folder contains the modified source code specific to our WinDivert integration. It mirrors the original RCE project structure for ease of integration. Only the files that were modified or added for the WinDivert integration are included.

- **NetworkingTests Feature File**: Located in the [NetworkingTests.feature](rce/de.rcenvironment.supplemental.testscriptrunner.scripts/resources/NetworkingTests.feature), this file introduces a new test, `@Network100`, which simulates network loss conditions.

- **InstanceNetworkingStepDefinitions**: The Java file [InstanceNetworkingStepDefinitions.java](win-divert-approach/rce/de.rcenvironment.supplemental.testscriptrunner/src/main/java/de.rcenvironment.extras.testscriptrunner.definitions.impl/InstanceNetworkingStepDefinitions.java) contains the step definitions for the new network test scenarios introduced in the NetworkingTests feature file.

## Getting Started

To integrate the WinDivert approach into your RCE project, follow these steps:

1. **Setup RCE**: Setup the RCE app by following the [RCE developer guide](https://updates-external.sc.dlr.de/rce/10.x/products/standard/releases/latest/documentation/windows/developer_guide.pdf)

2. **Include jDivert**: Ensure that jDivert is included in your project dependencies.

3. **Merge the rce Folder**: Integrate the contents of the `rce` folder with your existing RCE project. This involves merging the modified and new files with your project's corresponding directories.

4. **Test Implementation**: Execute the `@Network100` test in the NetworkingTests feature file to validate the integration and simulate the network loss scenario.

## Contribution

Contributions to this integration approach are welcome. Please adhere to the following guidelines in the main [README](../README.md).

## Support

For support or further inquiries about this WinDivert integration approach, contact luka.gerlach@smail.uni-koeln or akomaris@smail.uni-koeln.de
