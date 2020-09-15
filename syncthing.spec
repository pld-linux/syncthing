#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests

Summary:	Open Source Continuous File Synchronization
Name:		syncthing
Version:	1.9.0
Release:	1
# syncthing (MPLv2.0) bundles
# - angular, bootstrap, daterangepicker, fancytree, jQuery, moment (MIT),
# - ForkAwesome (MIT and OFL and CC-BY 3.0), and
# - a number of go packages (MIT and MPLv2.0 and BSD and ASL 2.0 and CC0 and ISC)
License:	MPLv2.0 and MIT and OFL and CC-BY and BSD and ASL 2.0 and CC0 and ISC
Group:		Applications/Networking
# Use official release tarball (contains vendored dependencies)
Source0:	https://github.com/syncthing/syncthing/releases/download/v%{version}/%{name}-source-v%{version}.tar.gz
# Source0-md5:	de188d86224e83d537c2a66f2f2dea71
URL:		https://syncthing.net/
BuildRequires:	golang >= 1.14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/syncthing/syncthing

%description
Syncthing replaces proprietary sync and cloud services with something
open, trustworthy and decentralized. Your data is your data alone and
you deserve to choose where it is stored, if it is shared with some
third party and how it's transmitted over the Internet.

%prep
%setup -qc

install -d build/src/$(dirname %{import_path})
mv %{name}/{AUTHORS,*.md} .
mv %{name} build/src/%{import_path}

%build
export GOPATH=$(pwd)/build
cd build/src/%{import_path}

go run build.go -version "v%{version}" -no-upgrade build
go run build.go -version "v%{version}" -no-upgrade install

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,5,7}}

cd build/src/%{import_path}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p man/*.7 $RPM_BUILD_ROOT%{_mandir}/man7

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/syncthing
%{_mandir}/man1/stdiscosrv.1*
%{_mandir}/man1/strelaysrv.1*
%{_mandir}/man1/syncthing.1*
%{_mandir}/man5/syncthing-config.5*
%{_mandir}/man5/syncthing-stignore.5*
%{_mandir}/man7/syncthing-bep.7*
%{_mandir}/man7/syncthing-device-ids.7*
%{_mandir}/man7/syncthing-event-api.7*
%{_mandir}/man7/syncthing-faq.7*
%{_mandir}/man7/syncthing-globaldisco.7*
%{_mandir}/man7/syncthing-localdisco.7*
%{_mandir}/man7/syncthing-networking.7*
%{_mandir}/man7/syncthing-relay.7*
%{_mandir}/man7/syncthing-rest-api.7*
%{_mandir}/man7/syncthing-security.7*
%{_mandir}/man7/syncthing-versioning.7*
