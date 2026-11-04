Name:           opencalc
Version:        1.0.0
Release:        1%{?dist}
Summary:        Modular C++ command-line calculator

License:        MIT
URL:            https://example.org/opencalc
Source0:        %{name}-%{version}.tar.gz

# Build dependencies are installed through Ubuntu APT.
# RPM dependency checking is disabled for this local build.

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make

%description
OpenCalc is a modular command-line calculator
written in C++17. It supports basic arithmetic
operations and modulo calculation.

%prep
%setup -q

%build
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr

cmake --build build --parallel 2

%install
mkdir -p %{buildroot}/usr/bin

install -m 0755 build/opencalc \
    %{buildroot}/usr/bin/opencalc

%files
/usr/bin/opencalc

%changelog
* Thu Nov 05 2026 Student <student@example.com> - 1.0.0-1
- Initial RPM package
- Added modulo operation
- Packaged modular C++ application
