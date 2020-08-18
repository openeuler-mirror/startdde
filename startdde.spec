%global with_debug 1
%global _unpackaged_files_terminate_build 0
%if 0%{?with_debug}
%global debug_package   %{nil}
%endif

Name:           startdde
Version:        5.4.0.1
Release:        2
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://shuttle.deepin.com/cache/repos/eagle/release-candidate/RERFNS4wLjAuMzUyOA/pool/main/s/startdde/
Source0:        %{name}_%{version}.orig.tar.xz

BuildRequires:  golang jq
BuildRequires:  dde-api
BuildRequires:  dde-api-devel
BuildRequires:  glib2-devel
BuildRequires:  libX11
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXcursor
BuildRequires:  libXfixes-devel
BuildRequires:  libXfixes
BuildRequires:  gtk3-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  alsa-lib

%{?systemd_requires}
Requires:       dde-daemon
Requires:       libcgroup-tools

%description
Startdde is used for launching DDE components and invoking user's
custom applications which compliant with xdg autostart specification.

%prep
%setup -q

sed -i '/polkit/s|lib|libexec|' watchdog/dde_polkit_agent.go
sed -i '/deepin-daemon/s|lib|libexec|' utils.go session.go misc/auto_launch/*.json

%build
export GOPATH=%{gopath}:%{_builddir}/%{name}-%{version}/vendor
BUILD_ID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
%make_build GOBUILD="go build -compiler gc -ldflags \"${LDFLAGS} -B $BUILD_ID\" -a -v -x"

%install
%make_install

%post
%systemd_post dde-readahead.service

%preun
%systemd_preun dde-readahead.service

%postun
%systemd_postun_with_restart dde-readahead.service

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/X11/Xsession.d/00deepin-dde-env
%{_sysconfdir}/X11/Xsession.d/01deepin-profile
%{_bindir}/%{name}
%{_sbindir}/deepin-fix-xauthority-perm
%{_datadir}/xsessions/deepin.desktop
%{_datadir}/lightdm/lightdm.conf.d/60-deepin.conf
%{_datadir}/%{name}/auto_launch.json
%{_datadir}/%{name}/memchecker.json
/usr/lib/deepin-daemon/greeter-display-daemon

%changelog
* Tue Aug 18 2020 chenbo pan <panchenbo@uniontech.com> - 5.4.0.1-2
- remove golang devel

* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0.1-1
- Package init
