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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,5,7}}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p man/*.7 $RPM_BUILD_ROOT%{_mandir}/man7

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS CONTRIBUTING.md
%attr(755,root,root) %{_bindir}/discosrv
%attr(755,root,root) %{_bindir}/relaysrv
%attr(755,root,root) %{_bindir}/stbench
%attr(755,root,root) %{_bindir}/stcompdirs
%attr(755,root,root) %{_bindir}/stdisco
%attr(755,root,root) %{_bindir}/stevents
%attr(755,root,root) %{_bindir}/stfileinfo
%attr(755,root,root) %{_bindir}/stfinddevice
%attr(755,root,root) %{_bindir}/stgenfiles
%attr(755,root,root) %{_bindir}/stindex
%attr(755,root,root) %{_bindir}/stsigtool
%attr(755,root,root) %{_bindir}/stvanity
%attr(755,root,root) %{_bindir}/stwatchfile
%attr(755,root,root) %{_bindir}/syncthing
%attr(755,root,root) %{_bindir}/testutil
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
