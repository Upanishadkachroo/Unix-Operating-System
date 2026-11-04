# Experiment: Creation of RPM Packages for C/C++ Applications

## 1. Aim

To study **RPM** (Red Hat Package Manager) packaging by selecting an open-source C/C++ project, modifying its source code to add a feature or fix a bug, compiling multiple source modules, and creating an **RPM** package for installation on a suitable Linux distribution.

Important: Since your local machine runs Ubuntu 24.04 **LTS**, we will perform the development and compilation on Ubuntu, install **RPM** packaging utilities, and generate an `.rpm` package without changing your operating system.

We will also compare **RPM** packaging with Debian (`.deb`) packaging.

## 2. Software and tools required

| Software         | Purpose                          |
| ---------------- | -------------------------------- |
| Ubuntu 24.04 LTS | Development environment          |
| GCC / G++        | C/C++ compilation                |
| Make             | Build automation                 |
| CMake            | Project configuration            |
| RPM              | Package management format        |
| rpmbuild         | RPM package creation             |
| Git              | Downloading open-source projects |
| Alien (optional) | RPM/DEB conversion               |

## 3. Introduction to RPM packaging

**RPM** stands for Red Hat Package Manager. It is a package management system used primarily by **RPM**-based Linux distributions.

**RPM** packages contain compiled executables, libraries, configuration files, documentation, and metadata required to install and manage software.

The **RPM** package file uses the extension:

``` .rpm ```

**RPM** packaging is commonly used in:

- Fedora
- Red Hat Enterprise Linux (**RHEL**)
- Rocky Linux
- AlmaLinux
- openSUSE

The `rpmbuild` utility is used to create **RPM** packages from source code using a specification file called a **SPEC** file.

[Growth: 全栈增长工程师指南 –](https://images.openai.com/static-rsc-4/HLDvtAKmGRKSQ_BDNUy-AvQueZdNSqFP4-FmiEIHlLau4SVMW5YjyDz3d_SsnxPMe4MKjLxZTrSf68hpi0erBZGY77oL8_nl9R0lJvnwF5I5MloTDMsmYOtbMRV5yik_scc2vP9GAJy8NG8iG4q9urAbYKQW18jOVS6W4vLnKt4?purpose=inline)

[growth.phodal.com](https://growth.phodal.com/?utm_source=chatgpt.com)

## 4. Selected open-source project

For this practical, we will use a small modular C++ application called OpenCalc, structured as a multi-source-file project.

The project will implement a command-line calculator with:

- Addition
- Subtraction
- Multiplication
- Division

We will add a new feature: Modulo operation (%).

This gives us a clear demonstration of:

## Multiple C++ source modules.

## Source-code modification. ## Compilation and linking. ## RPM SPEC file creation. ## Building and installing an RPM package.

The application will be released under the **MIT** License.

Note: OpenCalc below is a small educational **FOSS**-style project created for the packaging demonstration, not an existing third-party GitHub repository. This keeps the source and feature modification reproducible.

## 5. Installation of RPM packaging tools on Ubuntu

Open a terminal and execute:

Step 1: Update Ubuntu packages

``` sudo apt update sudo apt upgrade -y ```

Step 2: Install development and packaging utilities

```
sudo apt install -y \
    build-essential \
    cmake \
    git \
    rpm \
    rpm2cpio \
    cpio \
    tar \
    gzip
```

Step 3: Verify installation

``` g++ --version cmake --version rpm --version rpmbuild --version ```

Expected: **GCC**, CMake, **RPM** and rpmbuild version information should be displayed.

If `rpmbuild` is not found, check whether the Ubuntu **RPM** package provides it:

``` dpkg -L rpm | grep rpmbuild ```

The **RPM** build utility is available in Ubuntu's **RPM** tooling.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://manpages.ubuntu.com\&sz=32](https://www.google.com/s2/favicons?domain=https://manpages.ubuntu.com\&sz=32))

Build **RPM** Package(s)+1

Important distinction: Installing `rpm` on Ubuntu does not convert Ubuntu into an **RPM**-based distribution. We are only using **RPM** build tools to create packages. The resulting **RPM** should ideally be tested on a compatible Fedora or **RHEL**-family environment.

## 6. Create a multi-module C++ project

We will use the following project structure:

```
OpenCalc/
│
├── CMakeLists.txt
├── **LICENSE**
├── **README**.md
│
├── src/
│   ├── main.cpp
│   ├── calculator.cpp
│   └── calculator.h
│
└── tests/
    └── test_calculator.cpp
```

Each source file has a separate responsibility:

| File                | Responsibility                   |
| ------------------- | -------------------------------- |
| main.cpp            | Handles user input and output    |
| calculator.cpp      | Implements arithmetic operations |
| calculator.h        | Declares calculator functions    |
| test_calculator.cpp | Tests calculator operations      |
| CMakeLists.txt      | Defines the build configuration  |

### Step 1: Create the project directory

``` mkdir -p ~/**RPM**-Experiment/OpenCalc/src mkdir -p ~/**RPM**-Experiment/OpenCalc/tests

cd ~/**RPM**-Experiment/OpenCalc ```

### Step 2: Create the header file

``` nano src/calculator.h ```

Add:

``` #ifndef CALCULATOR_H #define CALCULATOR_H

namespace Calculator {
    double add(double a, double b);
    double subtract(double a, double b);
    double multiply(double a, double b);
    double divide(double a, double b);

    // New feature
    int modulo(int a, int b);
}

#endif ```

### Step 3: Create the implementation file

``` nano src/calculator.cpp ```

Add:

``` #include *calculator.h* #include <stdexcept>

namespace Calculator {

double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0)
    throw std::runtime_error(*Division by zero*);

    return a / b;
}

// Newly added feature
int modulo(int a, int b) {
    if (b == 0)
    throw std::runtime_error(*Modulo by zero*);

    return a % b;
}

} ```

### Step 4: Create the main program

``` nano src/main.cpp ```

Add:

``` #include <iostream> #include *calculator.h*

using namespace std;

int main() {
    double a, b;
    char op;

    cout << *OpenCalc - C++ Calculator\n*;

    cout << *Enter expression (e.g. 10 + 5): *;

    cin >> a >> op >> b;

    try {
    switch (op) {
    case '+':
    cout << Calculator::add(a, b);
    break;

    case '-':
    cout << Calculator::subtract(a, b);
    break;

    case '*':
    cout << Calculator::multiply(a, b);
    break;

    case '/':
    cout << Calculator::divide(a, b);
    break;

    case '%':
    if (a != static_cast<int>(a) ||
    b != static_cast<int>(b)) {
    throw runtime_error(
    *Modulo requires integers*
    );
    }

    cout << Calculator::modulo(
    static_cast<int>(a),
    static_cast<int>(b)
    );
    break;

    default:
    cout << *Invalid operator\n*;
    return 1;
    }
    }
    catch (const exception& e) {
    cerr << *Error: * << e.what() << '\n';
    return 1;
    }

    cout << '\n';
    return 0;
}
```

### Step 5: Create CMakeLists.txt

``` nano CMakeLists.txt ```

Add:

``` cmake_minimum_required(**VERSION** 3.16)

project(OpenCalc **VERSION** 1.0.0 **LANGUAGES** **CXX**)

set(CMAKE_CXX_STANDARD 17) set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(opencalc
    src/main.cpp
    src/calculator.cpp
)

target_include_directories(opencalc
    **PRIVATE** ${PROJECT_SOURCE_DIR}/src
)

install(
    **TARGETS** opencalc
    **RUNTIME** **DESTINATION** bin
)
```

### Step 6: Create the MIT License

``` nano **LICENSE** ```

Add the standard **MIT** License text, with your copyright holder and year.

This makes the educational project available under an open-source license. Do not describe it as an upstream **FOSS** project that you downloaded; it is an independently created project for the demonstration.

### Step 7: Create README

``` nano **README**.md ```

``` # OpenCalc

A modular command-line calculator written in C++17.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Modulo operation

## Build

mkdir build cd build cmake .. make

## Run

./opencalc

## License

**MIT** ```

## 7. Compile and test the application on Ubuntu

### Step 1: Configure the project

``` cd ~/**RPM**-Experiment/OpenCalc

cmake -S . -B build ```

### Step 2: Compile multiple C++ modules

``` cmake --build build -j$(nproc) ```

Here:

- `main.cpp` is compiled separately.
- `calculator.cpp` is compiled separately.
- The object files are linked into one executable.
- `-j$(nproc)` enables parallel compilation.

### Step 3: Execute the application

``` ./build/opencalc ```

Example:

``` OpenCalc - C++ Calculator Enter expression (e.g. 10 + 5): 10 + 5 15 ```

Test the newly added modulo feature:

``` OpenCalc - C++ Calculator Enter expression (e.g. 10 + 5): 10 % 3 1 ```

Test division by zero:

``` OpenCalc - C++ Calculator Enter expression (e.g. 10 + 5): 10 / 0 Error: Division by zero ```

Expected result

&#x20;The application should compile and execute successfully, including the newly implemented modulo operation.

## 8. Create the RPM package

Now we will convert the compiled C++ application into an **RPM** package.

### Step 1: Create the RPM directory structure

**RPM** uses a standard directory structure for packaging.

``` mkdir -p ~/rpmbuild/**BUILD** mkdir -p ~/rpmbuild/**RPMS** mkdir -p ~/rpmbuild/**SOURCES** mkdir -p ~/rpmbuild/**SPECS** mkdir -p ~/rpmbuild/**SRPMS** ```

The directory structure is:

``` ~/rpmbuild/ │ ├── **BUILD**/ ├── **RPMS**/ ├── **SOURCES**/ ├── **SPECS**/ └── **SRPMS**/ ```

| Directory | Purpose                           |
| --------- | --------------------------------- |
| BUILD     | Source extraction and compilation |
| RPMS      | Generated binary RPM packages     |
| SOURCES   | Source code archives and patches  |
| SPECS     | RPM specification files           |
| SRPMS     | Generated source RPM packages     |

This is the standard **RPM** build-tree organization.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.centos.org\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.centos.org\&sz=32))

CentOS Documentation+1

### Step 2: Create the source archive

First, create a properly named source directory and archive.

``` cd ~/**RPM**-Experiment

cp -r OpenCalc opencalc-1.0.0

tar -czf opencalc-1.0.0.tar.gz opencalc-1.0.0 ```

Copy the archive into the **RPM** source directory:

``` cp opencalc-1.0.0.tar.gz ~/rpmbuild/**SOURCES**/ ```

### Step 3: Create the RPM SPEC file

The **SPEC** file contains instructions for compiling, installing and packaging the application.

``` nano ~/rpmbuild/**SPECS**/opencalc.spec ```

Add the following:

``` Name:           opencalc Version:        1.0.0 Release:        1%{?dist} Summary:        Modular C++ command-line calculator

License:        **MIT** **URL**:            [https://example.org/opencalc](https://example.org/opencalc) Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++ BuildRequires:  cmake BuildRequires:  make

%description OpenCalc is a modular command-line calculator written in C++17. It supports basic arithmetic operations and modulo calculation.

%prep %setup -q

%build
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr

cmake --build build --parallel 2

%install mkdir -p %{buildroot}/usr/bin

install -m **0755** build/opencalc \
    %{buildroot}/usr/bin/opencalc

%files /usr/bin/opencalc

%changelog
- Thu Nov 05 **2026** Student <[student@example.com](mailto:student@example.com)> - 1.0.0-1
- Initial **RPM** package
- Added modulo operation
- Packaged modular C++ application
```

Explanation of important **SPEC** sections:

| Section       | Function                                |
| ------------- | --------------------------------------- |
| Name          | Package name                            |
| Version       | Software version                        |
| Release       | Package release number                  |
| Summary       | Short description                       |
| License       | Software license                        |
| Source0       | Source archive                          |
| BuildRequires | Required build dependencies             |
| %description  | Detailed package description            |
| %prep         | Extracts source code                    |
| %build        | Compiles the application                |
| %install      | Copies files into the packaging root    |
| %files        | Specifies files included in the package |
| %changelog    | Records package changes                 |

The **SPEC** file is the central instruction file used by `rpmbuild`.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://rpm.org\&sz=32](https://www.google.com/s2/favicons?domain=https://rpm.org\&sz=32))

Spec file format+1

Note: Replace the example project **URL** and author details with your own details before submission.

### Step 4: Build the RPM package

Execute:

``` rpmbuild -ba ~/rpmbuild/**SPECS**/opencalc.spec ```

Here:

- `-b` means build using a **SPEC** file.
- `-a` means build both binary and source packages.

The build process performs source extraction, compilation, installation into the build root, and package generation.

[42. Linux rpm 파일 만들기1 - 기본 spec 파일 작성 및 rpm 생성](https://images.openai.com/static-rsc-4/BI6BxZe7uJlZ6fpyfs0NZDBhqrTlz7aWHfTzFuYDxwfRBKxaaaAg7L2Xv9sLehjoue9XlLSJJEUDzuqzLbJfB6t_uOFdLkPX6EuwMYegZSOoSKTt_yJvfD191cF6WJBFY4K_fnDvU7b3hvj47m44zEbyuRvIy9BU9UclOusXbqg?purpose=inline)

[whitewing4139.tistory.com](https://whitewing4139.tistory.com/**287**?utm_source=chatgpt.com)

### Step 5: Locate the generated RPM package

``` find ~/rpmbuild/**RPMS** -type f -name **.rpm* ```

Expected directory:

```
rpmbuild/
└── **RPMS**/
    └── x86_64/
    └── opencalc-1.0.0-1.x86_64.rpm
```

The exact architecture suffix depends on your build environment.

### Step 6: Inspect the generated RPM

Display package information:

``` rpm -qpi ~/rpmbuild/**RPMS**/*/opencalc-*.rpm ```

List files included in the package:

``` rpm -qpl ~/rpmbuild/**RPMS**/*/opencalc-*.rpm ```

Verify package metadata:

``` rpm -K ~/rpmbuild/**RPMS**/*/opencalc-*.rpm ```

A locally generated package may report that it is not signed. This is not necessarily a build failure.

## 9. Test the RPM package on Ubuntu

Since Ubuntu uses Debian packaging natively, we should avoid treating **RPM** as its native installation mechanism.

We can safely extract and test the contents of our **RPM** package without installing it into the Ubuntu root filesystem.

### Step 1: Create a temporary extraction directory

``` mkdir -p ~/**RPM**-Experiment/rpm-test cd ~/**RPM**-Experiment/rpm-test ```

### Step 2: Extract the RPM

``` rpm2cpio ~/rpmbuild/**RPMS**/*/opencalc-*.rpm | cpio -idmv ```

### Step 3: Run the packaged executable

``` ./usr/bin/opencalc ```

Test:

``` OpenCalc - C++ Calculator Enter expression (e.g. 10 + 5): 15 % 4 3 ```

Package verification

The executable extracted from the **RPM** should work exactly like the original compiled executable.

For a proper deployment test, install the **RPM** in a Fedora virtual machine or container compatible with the package's target environment.

## 10. Comparison between RPM and Debian packaging

**RPM** and Debian are two major Linux software packaging formats.

[File:**RPM** Logo.svg - Wikimedia Commons](https://images.openai.com/static-rsc-4/PeedQkdS_hNzt1DSuNYa3Oob_TCium0RTO0bFnM86Hv4Eu5pcYVUrRAI-MqOW8RTBAcfytMybtbjQdTzj3IDrSjEGX20miMJ8b1Gm-pbtoPTJOzwyKt8Ca6hPljn9QZSom2NiJoOCg3dkGD4i3S2C-EGvEs9BUAy7H9Q7ahLcjI?purpose=inline)

**RPM**

### Red Hat Package Manager

`.rpm`

[Debian Logo **PNG** Transparent & **SVG** Vector - Freebie Supply](https://images.openai.com/static-rsc-4/tgGziLySZvo-f4hjr7VR44bOILYxz7nxN_7ZGKYeh_c_U25Ywmk2vA3jniE-VicnH_ALkQNW1ZR-Yk9x7DyynvyNhtKGhC2iZz_HW38dZzEbjaUjRV2CpvVb83-fVdRzqXJQXeIJUkNnUOszMC542lrmAVOIo2N110cG67Z6Dsk?purpose=inline)

Debian

Debian package format

`.deb`

| Parameter             | RPM packaging                | Debian packaging                                      |
| --------------------- | ---------------------------- | ----------------------------------------------------- |
| Package extension     | `.rpm`                       | `.deb`                                                |
| Package manager       | RPM                          | dpkg                                                  |
| High-level manager    | DNF / YUM / Zypper           | APT                                                   |
| Common distributions  | Fedora, RHEL, Rocky Linux    | Ubuntu, Debian, Linux Mint                            |
| Package build tool    | rpmbuild                     | dpkg-buildpackage                                     |
| Configuration file    | SPEC file                    | debian/control and other Debian files                 |
| Package installation  | rpm / dnf                    | dpkg / apt                                            |
| Dependency management | Requires, BuildRequires      | Depends, Build-Depends                                |
| Package database      | RPM database                 | dpkg database                                         |
| Package verification  | RPM signature/checksum tools | Debian package signatures and repository verification |
| Build output          | `.rpm`                       | `.deb`                                                |
| Source package        | `.src.rpm`                   | `.dsc`, source archives and Debian packaging files    |

### Advantages of RPM

## Provides structured package management.

## Supports dependency declarations. ## Supports package signing and verification. ## Supports binary and source packages. ## Provides SPEC files for automated builds. ## Supports upgrades and removal of packages.

### Advantages of Debian packaging

## Native to Ubuntu and Debian.

## Provides convenient package installation through APT. ## Supports dependency management. ## Supports source and binary packages. ## Provides standardized packaging rules. ## Integrates with Ubuntu software repositories.

### Which is suitable for Ubuntu?

For your local Ubuntu 24.04 machine:

- **DEB** packaging is the recommended native packaging format.
- **RPM** packaging is useful when preparing software for Fedora, **RHEL** or other **RPM**-based systems.

Both formats can package the same C/C++ application, but their metadata, build systems and installation mechanisms differ.

## 11. Demonstration of Debian packaging on Ubuntu (optional)

To understand the difference practically, we can package the same OpenCalc executable into a `.deb` file.

Create the directory structure:

``` mkdir -p ~/**RPM**-Experiment/deb-package/usr/bin ```

Copy the executable:

``` cp ~/**RPM**-Experiment/OpenCalc/build/opencalc \ ~/**RPM**-Experiment/deb-package/usr/bin/ ```

Create the Debian control directory:

``` mkdir -p ~/**RPM**-Experiment/deb-package/**DEBIAN** ```

Create the control file:

``` nano ~/**RPM**-Experiment/deb-package/**DEBIAN**/control ```

Add:

``` Package: opencalc Version: 1.0.0 Section: utils Priority: optional Architecture: amd64 Maintainer: Student <[student@example.com](mailto:student@example.com)> Description: Modular C++ command-line calculator A calculator supporting basic arithmetic operations and modulo calculation. ```

Build the Debian package:

``` cd ~/**RPM**-Experiment

dpkg-deb --build deb-package opencalc_1.0.0_amd64.deb ```

Install it on Ubuntu:

``` sudo apt install ./opencalc_1.0.0_amd64.deb ```

Run:

``` opencalc ```

Remove it:

``` sudo apt remove opencalc ```

Now you have demonstrated both package formats using the same application.

## 12. Result

The following outcomes are expected after completing the experiment:

## Installed GCC, CMake and RPM packaging utilities on Ubuntu 24.04.

## Created a modular C++ application containing multiple source files. ## Implemented a new modulo operation. ## Compiled and linked multiple C++ modules. ## Created an RPM SPEC file. ## Generated a binary `.rpm` package using `rpmbuild`. ## Inspected and extracted the RPM package. ## Created and installed a Debian `.deb` package on Ubuntu. ## Studied the differences between RPM and Debian packaging.

## 13. Conclusion

In this experiment, we studied **RPM** packaging for C/C++ applications using Ubuntu 24.04 as the development environment. We created a modular C++ calculator, added a new modulo feature, compiled the source files using CMake and generated an **RPM** package using the `rpmbuild` utility.

We also studied the **RPM** directory structure, **SPEC** file, package metadata and package verification. Finally, we compared **RPM** packaging with Debian packaging and demonstrated the creation of a `.deb` package using `dpkg-deb`.

Thus, we learned how multiple C/C++ source modules can be compiled, packaged and distributed as installable Linux software packages.

## 14. Screenshots to capture for your practical journal

| No. | Screenshot                                            |
| --- | ----------------------------------------------------- |
| 1   | Ubuntu terminal showing installed RPM tools           |
| 2   | OpenCalc project directory with multiple source files |
| 3   | C++ compilation using CMake                           |
| 4   | Calculator execution showing arithmetic operations    |
| 5   | Modulo feature execution                              |
| 6   | RPM directory structure                               |
| 7   | `opencalc.spec` file                                  |
| 8   | Successful `rpmbuild -ba` execution                   |
| 9   | Generated `.rpm` package                              |
| 10  | RPM package information using `rpm -qpi`              |
| 11  | RPM extraction and executable testing                 |
| 12  | Generated `.deb` package and installation on Ubuntu   |

## 15. Viva questions

Q1. What is **RPM**?

**RPM** stands for Red Hat Package Manager. It is a package management format used to distribute and install software on **RPM**-based Linux distributions.

Q2. What is rpmbuild?

It is a utility used to create **RPM** packages from source code and **SPEC** files.

Q3. What is a **SPEC** file?

A **SPEC** file contains package metadata and instructions for preparing, compiling, installing and packaging software.

Q4. What is the purpose of the **SOURCES** directory?

It stores source code archives and patches required during **RPM** package creation.

Q5. What is the difference between **RPM** and **DEB**?

**RPM** is primarily used by Fedora and **RHEL**-based distributions, whereas **DEB** is used by Debian and Ubuntu.

Q6. Can we create **RPM** packages on Ubuntu?

Yes. By installing **RPM** build utilities, we can create **RPM** packages on Ubuntu. However, compatibility should be verified on the intended **RPM**-based target distribution.

Q7. What is the purpose of CMake?

CMake generates build configurations and manages the compilation of multi-file C/C++ projects.

Q8. What is the difference between binary **RPM** and source **RPM**?

- Binary **RPM** contains compiled application files.
- Source **RPM** contains source code and packaging instructions required to rebuild the application.

Q9. What is BuildRoot?

BuildRoot is a temporary directory representing the target filesystem hierarchy where package files are staged before packaging.

**Q10**. Which packaging format should Ubuntu users prefer?

Debian (`.deb`) because Ubuntu natively uses **APT** and dpkg.

One important point for your submission: The OpenCalc example is an independently authored **MIT**-licensed educational project, rather than a downloaded upstream repository. If your examiner strictly requires an existing internet-hosted **FOSS** project, use an upstream C/C++ repository and document the exact source modification and attribution separately.

Official references:

- [**RPM** **SPEC** file documentation](https://rpm.org/docs/latest/manual/spec.html?utm_source=chatgpt.com)
- [Fedora **RPM** packaging guide](https://developer.fedoraproject.org/deployment/rpm/about.html?utm_source=chatgpt.com)
- [**RPM** Packaging Guide](https://rpm-packaging-guide.github.io/?utm_source=chatgpt.com)
- [Debian Policy Manual](https://[www.debian.org/doc/debian-policy/?utm_source=chatgpt.com](https://www.debian.org/doc/debian-policy/?utm_source=chatgpt.com))
- [Ubuntu rpmbuild manual](https://manpages.ubuntu.com/manpages/noble/man8/rpmbuild.8.html?utm_source=chatgpt.com)
