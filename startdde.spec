%global _missing_build_ids_terminate_build 0
%global debug_package   %{nil}

Name:           startdde
Version:        5.6.0.25
Release:        1
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/startdde
Source0:        %{name}-%{version}.tar.xz
Source1:        vendor.tar.gz

BuildRequires:  golang jq
BuildRequires:  dde-api
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
BuildRequires:  pkgconfig(gudev-1.0)

Requires:       dde-daemon
Requires:       libcgroup-tools

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}
sed -i 's|/usr/lib/deepin-daemon|/usr/libexec/deepin-daemon|g' \
misc/auto_launch/chinese.json misc/auto_launch/default.json
tar -xf %{SOURCE1}

%build


## Scripts in /etc/X11/Xsession.d are not executed after xorg start
sed -i 's|X11/Xsession.d|X11/xinit/xinitrc.d|g' Makefile
export GOPATH=%{_builddir}/%{name}-%{version}/vendor

%make_build GO_BUILD_FLAGS=-trimpath

%install
%make_install

%post
xsOptsFile=/etc/X11/Xsession.options
update-alternatives --install /usr/bin/x-session-manager x-session-manager \
    /usr/bin/startdde 90 || true
if [ -f $xsOptsFile ];then
	sed -i '/^use-ssh-agent/d' $xsOptsFile
	if ! grep '^no-use-ssh-agent' $xsOptsFile >/dev/null; then
		echo no-use-ssh-agent >> $xsOptsFile
	fi
fi

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/X11/xinit/xinitrc.d/00deepin-dde-env
%{_sysconfdir}/X11/xinit/xinitrc.d/01deepin-profile
%{_sysconfdir}/profile.d/deepin-xdg-dir.sh
%{_bindir}/%{name}
%{_sbindir}/deepin-fix-xauthority-perm
%{_datadir}/xsessions/deepin.desktop
%{_datadir}/lightdm/lightdm.conf.d/60-deepin.conf
%{_datadir}/%{name}/auto_launch.json
%{_datadir}/%{name}/memchecker.json
/usr/lib/deepin-daemon/greeter-display-daemon

%changelog
* Tue Jul 20 2021 weidong <weidong@uniontech.com> - 5.6.0.25-1
- update to 5.6.0.25-1

* Thu Sep 3 2020 weidong <weidong@uniontech.com> - 5.4.0.1-4
- fix source url in spec

* Wed Sep 2 2020 chenbo pan <panchenbo@uniontech.com> - 5.4.0.1-3
- fix requires golang devel

* Tue Aug 18 2020 chenbo pan <panchenbo@uniontech.com> - 5.4.0.1-2
- remove golang devel

* Thu Jul 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0.1-1
- Package init
