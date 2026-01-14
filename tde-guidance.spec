%bcond clang 1
%bcond xscreensaver 1
%bcond powermanager 0

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.4
%endif
%define pkg_rel 2

%define tde_pkg tde-guidance
%define tde_prefix /opt/trinity


%define __arch_install_post %{nil}

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.8.0svn20080103
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	A collection of system administration tools for Trinity
Group:		Applications/Utilities
URL:		http://www.simonzone.com/software/guidance

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/settings/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		trinity-%{tde_pkg}-rpmlintrc

BuildSystem:  cmake 

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} -isystem %{tde_prefix}/include"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:	trinity-pytdeextensions
BuildRequires:	trinity-libpythonize0-devel
BuildRequires:	trinity-pytde
BuildRequires:	chrpath

BuildRequires:	libtool

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SIP support
BuildRequires:	sip4-tqt-devel >= 4.10.5
Requires:		sip4-tqt >= 4.10.5

# PYTHON-QT support
BuildRequires:	pytqt-devel
BuildRequires:	trinity-pytde-devel
BuildRequires:	trinity-pytqt-tools

# XSCREENSAVER support
#  RHEL 4: disabled
#  RHEL 6: available in EPEL
#  RHEL 7: available in NUX
#  RHEL 8: available in EPEL
#  RHEL 9: available in EPEL
%if %{with xscreensaver}
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:	xscreensaver
BuildRequires:	xscreensaver-base
BuildRequires:	xscreensaver-gl
%endif

# PYTHON support
%if "%{?python}" == "%{nil}"
%global python python3
%endif
%global __python %__python3
%global python_sitearch %{python3_sitearch}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
BuildRequires:	pkgconfig(python)
BuildRequires:	%{python}-setuptools

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrender)

Requires:		pytqt
Requires:		trinity-pytde
Requires:		trinity-pytdeextensions
Requires:		hwdata

Requires:		%{name}-backends = %{?epoch:%{epoch}:}%{version}-%{release}

# POWERMANAGER support (requires HAL)
#define with_powermanager 1
Obsoletes:	trinity-tde-guidance-powermanager < %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:		trinity-guidance < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-guidance = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Guidance currently consists of four programs designed to help you
look after your system:
 o  userconfig - User and Group administration
 o  serviceconfig - Service/daemon administration
 o  mountconfig - Disk and filesystem administration

These tools are available in Trinity Control Center, System Settings 
or can be run as standalone applications.

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{tde_prefix}/bin/mountconfig
%{tde_prefix}/bin/serviceconfig
%{tde_prefix}/bin/userconfig
%attr(0644,root,root) %{tde_prefix}/%{_lib}/trinity/*.so
%attr(0644,root,root) %{tde_prefix}/%{_lib}/trinity/*.la
%{tde_prefix}/share/apps/guidance/
%{tde_prefix}/share/applications/tde/*.desktop
%{tde_prefix}/share/icons/crystalsvg/*/*/*.png
%{python_sitelib}/tde-guidance/SMBShareSelectDialog.py*
%{python_sitelib}/tde-guidance/SimpleCommandRunner.py*
%{python_sitelib}/tde-guidance/fuser.py*
%{python_sitelib}/tde-guidance/fuser_ui.py*
%{python_sitelib}/tde-guidance/mountconfig.py*
%{python_sitelib}/tde-guidance/serviceconfig.py*
%{python_sitelib}/tde-guidance/sizeview.py*
%{python_sitelib}/tde-guidance/unixauthdb.py*
%{python_sitelib}/tde-guidance/userconfig.py*

# Files from powermanager
%if %{with powermanager}
%exclude %{tde_prefix}/share/icons/hicolor/22x22/apps/power-manager.png
%exclude %{tde_prefix}/share/apps/guidance/pics/ac-adapter.png
%exclude %{tde_prefix}/share/apps/guidance/pics/battery*.png
%exclude %{tde_prefix}/share/apps/guidance/pics/processor.png
%endif

%{tde_prefix}/share/doc/tde/HTML/en/tde-guidance/
%{tde_prefix}/share/man/man1/mountconfig-trinity.1*
%{tde_prefix}/share/man/man1/serviceconfig-trinity.1*
%{tde_prefix}/share/man/man1/userconfig-trinity.1*

##########

%package backends
Group:			Applications/Utilities
Summary:		collection of system administration tools for GNU/Linux [Trinity]
Requires:		hwdata
Requires:		%{python}

Obsoletes:		trinity-guidance-backends < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-guidance-backends = %{?epoch:%{epoch}:}%{version}-%{release}

%description backends
This package contains the platform neutral backends used in the
Guidance configuration tools.

%files backends
%defattr(-,root,root,-)
%dir %{python_sitelib}/tde-guidance
%{python_sitelib}/tde-guidance/MicroHAL.py*


##########

%if %{with powermanager}

%package powermanager
Group:			Applications/Utilities
Summary:		HAL based power manager applet [Trinity]
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		hal

Obsoletes:		trinity-guidance-powermanager < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-guidance-powermanager = %{?epoch:%{epoch}:}%{version}-%{release}

%if "%{tde_prefix}" == "/usr"
Conflicts:	guidance-power-manager
Conflicts:	kde-guidance-powermanager
%endif

%description powermanager
A power management applet to indicate battery levels and perform hibernate or
suspend using HAL.

%files powermanager
%defattr(-,root,root,-)
%{tde_prefix}/bin/guidance-power-manager
%{python_sitelib}/tde-guidance/MicroHAL.py*
%{python_sitelib}/tde-guidance/guidance-power-manager.py*
%{python_sitelib}/tde-guidance/powermanage.py*
%{python_sitelib}/tde-guidance/gpmhelper.py*
%{python_sitelib}/tde-guidance/powermanager_ui.py*
%{python_sitelib}/tde-guidance/guidance_power_manager_ui.py*
%{python_sitelib}/tde-guidance/notify.py*
%{python_sitelib}/tde-guidance/tooltip.py*
%{python_sitelib}/tde-guidance/__pycache__/MicroHAL.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/guidance-power-manager.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/powermanage.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/gpmhelper.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/powermanager_ui.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/guidance_power_manager_ui.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/notify.*.pyc
%{python_sitelib}/tde-guidance/__pycache__/tooltip.*.pyc
%{tde_prefix}/share/icons/hicolor/22x22/apps/power-manager.png
%{tde_prefix}/share/apps/guidance/pics/ac-adapter.png
%{tde_prefix}/share/apps/guidance/pics/battery*.png
%{tde_prefix}/share/apps/guidance/pics/processor.png
%{tde_prefix}/share/autostart/guidance-power-manager.desktop

%endif

%conf -p
%__sed -i "userconfig/unixauthdb.py" \
  -e "s|self.first_uid = .*|self.first_uid = 500|" \
  -e "s|self.first_gid = .*|self.first_gid = 500|"

unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


