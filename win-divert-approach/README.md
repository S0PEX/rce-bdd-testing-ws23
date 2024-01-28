# WinDivert approach

this directory contains everything to get started with our WinDivert approach to integrate network tests into the RCE application.

## Prerequisites

To get started, you need to include the WinDivert Java binding [jDivert](https://mvnrepository.com/artifact/com.github.ffalcinelli/jdivert) into the RCE project.

## Structure

The [rce](rce) folder contains the source code for our WinDivert approach. We only uploaded the files we touched, still adhering to the original rce structure.

The [NetworkingTests](rce/de.rcenvironment.supplemental.testscriptrunner.scripts/resources/NetworkingTests.feature) feature file contains a new test `@Network100` where a simulation loss is simulated.

The [InstanceNetworkingStepDefinitions](win-divert-approach/rce/de.rcenvironment.supplemental.testscriptrunner/src/main/java/de.rcenvironment.extras.testscriptrunner.definitions.impl/InstanceNetworkingStepDefinitions.java) file contains the corresponding new step definitions.