%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%define specrelease 5%{?dist}
%if 0%{?openeuler}
%define specrelease 5
%endif

Name:           startdde
Version:        5.8.11.3
Release:        %{specrelease}
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/startdde
Source0:        %{name}-%{version}.tar.xz
Source1:        vendor.tar.gz

BuildRequires:  golang
BuildRequires:  jq
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  gtk3-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  dde-api-devel
BuildRequires:  libsecret-devel

Provides:       x-session-manager
Requires:       dde-daemon
Requires:       procps
Requires:       deepin-desktop-schemas
Requires:       dde-kwin
Requires:       libXfixes
Requires:       libXcursor
Requires:       libsecret
Recommends:     dde-qt5integration

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version}
sed -i 's|/usr/lib/deepin-daemon|/usr/libexec/deepin-daemon|g' \
misc/auto_launch/chinese.json misc/auto_launch/default.json

patch Makefile < rpm/Makefile.patch
patch main.go < rpm/main.go.patch
tar -xf %{SOURCE1}

%build
export GOPATH=%{_builddir}/%{name}-%{version}/vendor:$GOPATH
## Scripts in /etc/X11/Xsession.d are not executed after xorg start
sed -i 's|X11/Xsession.d|X11/xinit/xinitrc.d|g' Makefile

%make_build GO_BUILD_FLAGS='-trimpath -ldflags "-s" -buildmode=pie'

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
%{_datadir}/%{name}/app_startup.conf
%{_datadir}/%{name}/filter.conf
%{_datadir}/glib-2.0/schemas/com.deepin.dde.display.gschema.xml
%{_datadir}/glib-2.0/schemas/com.deepin.dde.startdde.gschema.xml
/usr/lib/deepin-daemon/greeter-display-daemon

%changelog
* Wed Jun 28 2023 liweigang <liweiganga@uniontech.com> - 5.8.11.3-5
- feat: update vendor(update golang.org/x/sys)

* Mon Apr 03 2023 liweiganga <liweiganga@uniontech.com> - 5.8.11.3-4
- feat: fix pie

* Tue Mar 14 2023 liweiganga <liweiganga@uniontech.com> - 5.8.11.3-3
- feat: fix strip

* Wed Dec 21 2022 liweiganga <liweiganga@uniontech.com> - 5.8.11.3-2
- enable debuginfo for fix strip

* Tue Jul 19 2022 konglidong <konglidong@uniontech.com> - 5.8.11.3-1
- update to 5.8.11.3

* Thu Aug 26 2021 zhangkea <zhangkea@uniontech.com> - 5.6.0.25-2
- Update vendor

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
