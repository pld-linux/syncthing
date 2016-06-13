#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests

Summary:	Open Source Continuous File Synchronization
Name:		syncthing
Version:	0.13.7
Release:	0.1
License:	MPL-2.0
Group:		Applications/Networking
Source0:	https://github.com/syncthing/syncthing/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9a94fa95428d4191f61eed834a8161be
URL:		https://syncthing.net/
BuildRequires:	golang >= 1.3.1
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
%setup -q

GOPATH=$(pwd)/src
install -d $(dirname $GOPATH/%{import_path})
ln -s ../../.. $GOPATH/%{import_path}
ln -s .. vendor/src

%build
export GOPATH=$(pwd)
cd src/%{import_path}
go run build.go -version "v%{version}" -no-upgrade

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/syncthing $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/syncthing
