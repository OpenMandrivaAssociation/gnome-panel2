%define req_libwnck_version 2.19.5
%define req_libglade_version 2.5.0
%define req_gconf2_version 2.31.6
%define req_gnomeui_version 2.5.4
%define req_gtk_version 2.19.7
%define req_glib_version 2.15.5
%define req_gnomedesktop_version 2.11.1

%define api_version 2
%define api2 3
%define lib_major   0
%define libname %mklibname panel-applet- %{api_version} %{lib_major}
%define libname2 %mklibname panel-applet- %{api2} %{lib_major}
%define libnamedev %mklibname -d panel-applet- %{api_version}

%define in_process_applets 0
%define oname gnome-panel

Summary:	The core programs for the GNOME GUI desktop environment
Name:		gnome-panel2
Version:	2.32.1
Release:	9
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{oname}-%{version}.tar.bz2
Source1:	mandriva-panel.png

# (fc) 2.0.1-2mdk  use xlock instead of xscreensaver to lock root desktop
Patch0:		gnome-panel-2.27.91-rootlock.patch
# (fc) 2.0.1-2mdk  Mandriva customization
Patch1:		gnome-panel-mdvcustomizations.patch
Patch2:		gnome-panel-2.32.1-fix-linking.patch
# (fc) 2.19.6-2mdv use beagle or tracker (if available) as search tool by default (Fedora)
Patch16:	gnome-panel-2.27.91-search.patch
# (fc) 2.28.0-3mdv ensure net_applet role is network
Patch19:	gnome-panel-2.29.92-netapplet.patch
# (fc) allow more bookmarks before switching to submenus
Patch20:	bookmarks-submenu.patch
# (fc) add about-mandriva menu entry if available
Patch21:	gnome-panel-2.28.0-about-mandriva.patch
# (fc) add padding for icons on panel (GNOME bug #343436) (Fedora)
Patch22:	gnome-panel-2.30.0-panel-padding.patch
# (fc) add padding for icons in notification area (GNOME bug #583273)
Patch23:	gnome-panel-2.31.6-icon-padding.patch
Patch24:	gnome-panel-2.32.1-automake-1.13.patch
URL:		https://www.gnome.org/
BuildRequires:	pkgconfig(gnome-desktop-2.0) >= %{req_gnomedesktop_version}
BuildRequires:	pkgconfig(libglade-2.0) >= %{req_libglade_version}
BuildRequires:	pkgconfig(libwnck-1.0) >= %{req_libwnck_version}
BuildRequires:	pkgconfig(xres)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	libgweather2-devel >= 2.27.90
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	rarian
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	libxslt-proc
BuildRequires:	pkgconfig(glib-2.0) >= %{req_glib_version}
BuildRequires:	pkgconfig(gtk+-2.0) >= %{req_gtk_version}
BuildRequires:	pkgconfig(libgnomeui-2.0) >= %{req_gnomeui_version}
BuildRequires:	pkgconfig(gconf-2.0) >= %{req_gconf2_version}
BuildRequires:	gnome-menus2-devel >= 2.27.92
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc
BuildRequires:	gnome-common
BuildRequires:	intltool
Requires(post):	scrollkeeper
Requires(postun): scrollkeeper
Requires:	gnome-session
Requires:	gnome-desktop
Requires:	polkit-agent
Requires:	GConf2 >= %{req_gconf2_version}
Suggests:	gnome-applets
Requires:	glib2 >= %{req_glib_version}
Requires:	gnome-menus2
Requires:	alacarte

# for screen locking and search function in panel
Requires:	gnome-utils
Requires:	gnome-screensaver
Requires:	desktop-common-data
#(patch0)
Requires:	xlockmore

%description
GNOME (GNU Network Object Model Environment) is a user-friendly
set of applications and desktop tools to be used in conjunction with a
window manager for the X Window System.  GNOME is similar in purpose and
scope to CDE and KDE, but GNOME is based completely on free
software. 

The GNOME panel packages provides the gnome panel, menus and some
basic applets for the panel.

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n	%{libname}
Panel libraries for running GNOME panels.

%package -n	%{libname2}
Summary:	%{summary}
Group:		System/Libraries
Provides:	libpanel-applet-%{api2} = %{version}-%{release}

%description -n	%{libname2}
Panel libraries for running GNOME panels.

%package -n	%{libnamedev}
Summary:	Static libraries, include files for GNOME panel
Group:		Development/GNOME and GTK+
Provides:	libpanel-applet-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	%{libname2} = %{version}-%{release}
Obsoletes:	%{mklibname -d panel-applet- 2 0} < 2.32.1-6

%description -n	%{libnamedev}
Panel libraries and header files for creating GNOME panels.

%prep
%setup -q -n %{oname}-%{version}
%autopatch -p1

#needed by patch2,patch23,patch24
autoreconf

%build
%configure2_5x --disable-eds --disable-scrollkeeper \
--disable-static \
%if %{in_process_applets}
--with-in-process-applets=all
%endif

make LIBS="-lgmodule-2.0"

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/gnome-panel/pixmaps-
#remove old files
rm -rf %{buildroot}%{_datadir}/omf/gnome-panel

%find_lang %{oname}-2.0 --with-gnome --all-name

#remove unpackaged files
rm -rf %{buildroot}%{_datadir}/gnome-panelrc %{buildroot}%{_localstatedir}/lib/scrollkeeper


%define schemas clock fish panel-compatibility panel-general panel-global panel-object panel-toplevel window-list workspace-switcher notification_area_applet

%post
%update_scrollkeeper 
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --recursive-unset /apps/panel > /dev/null 2> /dev/null
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --recursive-unset /schemas/apps/panel > /dev/null 2> /dev/null

%post_install_gconf_schemas %{schemas}
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries > /dev/null
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries /apps/panel > /dev/null

%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}

%postun
%clean_scrollkeeper
%clean_icon_cache hicolor

%files -f %{oname}-2.0.lang
%doc AUTHORS COPYING NEWS README
%{_sysconfdir}/gconf/schemas/clock.schemas
%{_sysconfdir}/gconf/schemas/fish.schemas
%{_sysconfdir}/gconf/schemas/panel-compatibility.schemas
%{_sysconfdir}/gconf/schemas/panel-general.schemas
%{_sysconfdir}/gconf/schemas/panel-global.schemas
%{_sysconfdir}/gconf/schemas/panel-object.schemas
%{_sysconfdir}/gconf/schemas/panel-toplevel.schemas
%{_sysconfdir}/gconf/schemas/window-list.schemas
%{_sysconfdir}/gconf/schemas/workspace-switcher.schemas
%{_sysconfdir}/gconf/schemas/notification_area_applet.schemas
%{_sysconfdir}/gconf/schemas/panel-default-setup.entries

%{_bindir}/*
%{_libexecdir}/gnome-panel-add
%if %{in_process_applets}
%dir %{_libexecdir}/gnome-panel
%dir %{_libexecdir}/gnome-panel/*.so
%else
%{_libexecdir}/clock-applet
%{_libexecdir}/fish-applet
%{_libexecdir}/notification-area-applet
%{_libexecdir}/wnck-applet
%{_datadir}/dbus-1/services/org.gnome.panel.applet.ClockAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.FishAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.NotificationAreaAppletFactory.service
%{_datadir}/dbus-1/services/org.gnome.panel.applet.WnckletFactory.service
%endif
%{_libdir}/gnome-panel/modules
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gnome
%dir %{_datadir}/gnome/help
%{_datadir}/gnome-panel
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/idl/*
%{_datadir}/icons/hicolor/*/apps/*

%files -n %{libname}
%{_libdir}/libpanel-applet-%{api_version}.so.%{lib_major}*

%files -n %{libname2}
%{_libdir}/libpanel-applet-%{api2}.so.%{lib_major}*
%{_libdir}/girepository-1.0/PanelApplet-3.0.typelib

%files -n %{libnamedev}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/libpanel*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/PanelApplet-3.0.gir


