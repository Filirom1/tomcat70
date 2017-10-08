# If the build is running on copr
%if 0%{?copr_username:1}

# define your copr_username and copr_projectname
%global scl %{copr_username}-%{copr_projectname}

# For other build systems, define the provider and the name of the SCL, e.g. myorganization-ruby193
%else
%global scl_name_prefix toto-
%global scl_name_base tomcat
%global scl_name_version 70

%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}
%endif


%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}

# Optional but recommended: define nfsmountable
%global nfsmountable 1

%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 0.0.5
Release: 1%{?dist}
License: GPLv2+
Requires: %{scl_prefix}tomcat
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

# This is only needed when you want to provide an optional scldevel subpackage
%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially useful for development of
packages depending on %scl Software Collection.

%prep
%setup -c -T

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH="%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LD_LIBRARY_PATH="%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}"
EOF

# This is only needed when you want to provide an optional scldevel subpackage
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install the generated man page
mkdir -p %{buildroot}%{_mandir}/man7/
#install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

mkdir %{buildroot}/%{_scl_prefix}

%files

%files runtime -f filelist
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Sat Oct 07 2017 Romain Philibert <Filirom1@gmail.com> 0.0.5-1
- move spec (Filirom1@gmail.com)
- Update README.md (filirom1@gmail.com)

* Sat Oct 07 2017 Romain Philibert <Filirom1@gmail.com> 0.0.4-1
- remove toto-tomcat70-less dependency

* Sat Oct 07 2017 Romain Philibert <Filirom1@gmail.com> 0.0.3-1
- wip scl (Filirom1@gmail.com)

* Sat Oct 07 2017 Romain Philibert <Filirom1@gmail.com> 0.0.2-1
- new package built with tito

* Fri Aug 30 2013 John Doe &lt;jdoe@example.com&gt; 1-1
- Initial package
