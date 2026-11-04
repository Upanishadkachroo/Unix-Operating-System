# Experiment: Create a Debian package for a modular C/C++ FOSS project

Since your system is Ubuntu 24.04, Debian packaging is the native approach. The output will be a `.deb` package, built using tools such as `dpkg-buildpackage` and `debhelper`.

For this experiment, we should use an actual upstream **FOSS** project, make a small documented feature change, and package the modified source. This is different from the earlier OpenCalc **RPM** exercise: OpenCalc was an independently created demonstration project, not a project pulled from an upstream **FOSS** repository.

I recommend doing the Debian experiment in C++ so you can reuse your existing C++ build experience. The same Debian packaging structure can also package C or Java applications.

## 1. Selected upstream project: TinyXML-2

Use TinyXML-2, a real open-source C++ **XML** parser. Its upstream repository is [leethomason/tinyxml2 on GitHub](https://github.com/leethomason/tinyxml2?utm_source=chatgpt.com). It is a C++ library with CMake build support, and Debian already packages it as separate runtime and development packages. That makes it a useful example for understanding multi-file C++ builds and package contents.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://packages.debian.org\&sz=32](https://www.google.com/s2/favicons?domain=https://packages.debian.org\&sz=32))

packages.debian.org+1

Proposed feature for the practical: add a small **XML** inspection utility that uses TinyXML-2 to read an **XML** file and display its root element and child elements. We can keep the utility in separate C++ source/header files, then package the executable and its runtime dependency. This demonstrates a feature addition without pretending that the feature already exists in upstream TinyXML-2.

## 2. Install Debian packaging tools

Run on Ubuntu:

``` sudo apt update

sudo apt install -y \
    build-essential \
    cmake \
    git \
    dpkg-dev \
    debhelper \
    devscripts \
    dh-make \
    lintian \
    fakeroot \
    libtinyxml2-dev
```

These tools serve different purposes:

| Tool                | Purpose                                            |
| ------------------- | -------------------------------------------------- |
| `dpkg-buildpackage` | Builds Debian source and binary packages           |
| `debhelper`         | Automates packaging tasks                          |
| `dh`                | Runs the debhelper sequence                        |
| `dpkg-deb`          | Inspects and builds `.deb` archives                |
| `lintian`           | Checks package quality                             |
| `fakeroot`          | Simulates file ownership during packaging          |
| `libtinyxml2-dev`   | Provides TinyXML-2 headers and development library |

Debian's recommended workflow uses an upstream source tree, a `debian/` packaging directory, and `dpkg-buildpackage`.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://wiki.debian.org\&sz=32](https://www.google.com/s2/favicons?domain=https://wiki.debian.org\&sz=32))

Debian Wiki+2

## 3. Download the FOSS source

Keep this experiment separate from your earlier **RPM** work:

``` mkdir -p ~/Debian-Experiment cd ~/Debian-Experiment

git clone [https://github.com/leethomason/tinyxml2.git](https://github.com/leethomason/tinyxml2.git) cd tinyxml2

git status ls ```

Inspect the project structure and build configuration:

``` find . -maxdepth 2 -type f | sort | head -80 ```

Check the upstream license and version:

``` ls **LICENSE*** grep -n *project(* CMakeLists.txt ```

Build the unmodified upstream project first:

``` cmake -S . -B build -DCMAKE_BUILD_TYPE=Release cmake --build build -j$(nproc) ```

This establishes that the original **FOSS** source builds before we introduce our feature.

## 4. Add the feature using multiple C++ modules

After the original TinyXML-2 build succeeds, create a separate utility inside the repository:

``` mkdir -p tools/xml-inspector cd tools/xml-inspector

touch main.cpp xml_inspector.cpp xml_inspector.h ```

The utility will have this structure:

``` tinyxml2/ ├── CMakeLists.txt ├── tinyxml2.cpp ├── tinyxml2.h ├── tools/ │   └── xml-inspector/ │       ├── main.cpp │       ├── xml_inspector.cpp │       └── xml_inspector.h └── debian/ ```

The new feature will be:

- Accept an **XML** filename as a command-line argument.
- Parse the **XML** document using TinyXML-2.
- Display the root element.
- Display its immediate child elements.
- Display an error if the file cannot be opened or parsed.

This gives you a multi-module C++ application with a genuine upstream **FOSS** library as its foundation.

Important: Keep the upstream source and license intact. Document your added files and feature separately. Do not claim your new utility is an existing upstream TinyXML-2 feature.

## 5. Debian packaging directory

Once the feature builds and runs, create the Debian metadata directory in the project root:

``` cd ~/Debian-Experiment/tinyxml2 mkdir -p debian ```

A Debian source package uses files in `debian/` to describe the package, dependencies, build procedure, copyright, and changelog.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://wiki.debian.org\&sz=32](https://www.google.com/s2/favicons?domain=https://wiki.debian.org\&sz=32))

Debian Wiki+1

The important files are:

```
debian/
├── control
├── changelog
├── rules
├── copyright
└── source/
    └── format
```

For a package named `xml-inspector`, the key files can follow this pattern.

`debian/control`

``` Source: xml-inspector Section: utils Priority: optional Maintainer: Student <[student@example.com](mailto:student@example.com)> Build-Depends: debhelper-compat (= 13), cmake, g++, libtinyxml2-dev Standards-Version: 4.6.2 Rules-Requires-Root: no

Package: xml-inspector Architecture: any Depends: ${shlibs:Depends}, ${misc:Depends} Description: **XML** inspection utility using TinyXML-2 A command-line utility that parses **XML** documents and displays their root and child elements. ```

`debian/rules`

``` #!/usr/bin/make -f

%:
	dh $@ --buildsystem=cmake
```

The command below makes the rules file executable:

``` chmod +x debian/rules ```

`debian/source/format`

``` 3.0 (quilt) ```

`debian/changelog`

``` xml-inspector (1.0.0-1) unstable; urgency=medium

    * Initial Debian package.
    * Added **XML** inspection functionality.
    * Used TinyXML-2 for **XML** parsing.

-- Student <[student@example.com](mailto:student@example.com)>  Thu, 05 Nov **2026** 08:00:00 +**0530** ```

Use your actual name and email in the maintainer fields.

`debian/copyright` must accurately describe the upstream TinyXML-2 license and the copyright/license of your added utility. Do not simply label the entire combined project **MIT** or **GPL** without checking the upstream license.

The `debian/rules` file above assumes that your root CMake configuration builds and installs the `xml-inspector` executable. We will need to configure that before building the package.

## 6. Build the Debian package

After the application and packaging metadata are ready:

``` cd ~/Debian-Experiment/tinyxml2

dpkg-buildpackage -us -uc -b ```

Options:

- `-b`: Build binary packages.
- `-us`: Do not sign the source package.
- `-uc`: Do not sign the `.changes` file.

The resulting `.deb` should appear in the parent directory.

``` cd .. find . -maxdepth 1 -name **.deb* ```

Inspect the generated package:

``` dpkg-deb --info xml-inspector_1.0.0-1_amd64.deb dpkg-deb --contents xml-inspector_1.0.0-1_amd64.deb ```

Install and test:

``` sudo apt install ./xml-inspector_1.0.0-1_amd64.deb

xml-inspector sample.xml ```

Remove it after testing:

``` sudo apt remove xml-inspector ```

For a quality check, run:

``` lintian ../xml-inspector_1.0.0-1_amd64.changes ```

The exact generated filenames may differ depending on your package version and architecture.

## 7. Comparison of RPM and Debian packaging

This is the comparison you can write on your practical answer sheet.

| Parameter                  | RPM packaging                              | Debian packaging                         |
| -------------------------- | ------------------------------------------ | ---------------------------------------- |
| Package extension          | `.rpm`                                     | `.deb`                                   |
| Common distributions       | Fedora, RHEL, Rocky Linux, AlmaLinux       | Debian, Ubuntu, Linux Mint               |
| Package manager            | RPM                                        | DPKG                                     |
| High-level package manager | DNF, YUM, Zypper                           | APT                                      |
| Build command              | `rpmbuild`                                 | `dpkg-buildpackage`                      |
| Package specification      | `.spec` file                               | `debian/` directory                      |
| Main metadata              | SPEC file                                  | `debian/control`                         |
| Build dependencies         | `BuildRequires`                            | `Build-Depends`                          |
| Runtime dependencies       | `Requires`                                 | `Depends`                                |
| Build scripts              | SPEC sections such as `%build`, `%install` | `debian/rules`                           |
| Binary package             | `.rpm`                                     | `.deb`                                   |
| Source package             | `.src.rpm`                                 | `.dsc` with source archives              |
| Package inspection         | `rpm -qpi`, `rpm -qpl`                     | `dpkg-deb --info`, `dpkg-deb --contents` |
| Installation               | `rpm -i` or `dnf install`                  | `dpkg -i` or `apt install`               |
| Removal                    | `rpm -e` or `dnf remove`                   | `dpkg -r` or `apt remove`                |
| Package database           | RPM database                               | DPKG database                            |

### Important differences

## RPM uses a single `.spec` file to define package metadata and build instructions. Debian uses multiple files inside the `debian/` directory.

## Debian packaging commonly uses `debhelper` to automate building, installation, dependency generation, and package creation. ## APT can automatically resolve and install dependencies from configured repositories. DNF provides similar dependency resolution for RPM-based distributions. ## Both systems support source packages, binary packages, dependency management, installation, upgrades, and removal. ## RPM packages are commonly used in Fedora/RHEL-based systems, while DEB packages are native to Ubuntu and Debian.

## 8. Result and conclusion for the practical journal

Result: The upstream **FOSS** source code was obtained, a new feature was added using modular C++ code, and the application was prepared for Debian packaging using `dpkg-buildpackage`. The generated `.deb` package was inspected, installed, and tested on Ubuntu.

Conclusion: Debian packaging provides a standardized method to distribute C, C++, and Java applications on Debian-based Linux distributions. **RPM** and Debian packaging perform similar functions but use different package formats, build tools, metadata files, and package-management systems.

## Next step

First run the installation, clone, and original build commands from sections 2 and 3. Send me the output of `find . -maxdepth 2 -type f | sort` and the CMake build result. I can then give you the exact feature implementation and CMake changes for the version of TinyXML-2 you have downloaded, before we create the `.deb` package.
