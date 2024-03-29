# TODO:
#  - fix unresolved symbols in post check
#
# Conditional build:
%bcond_without  gtk3            # build without GTK+3

Summary:	Gnome-mplayer toolkit
Name:		gmtk
Version:	1.0.8
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://gmtk.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	ee8ab99f3ac2e0071c99a35e4847bba5
URL:		http://kdekorte.googlepages.com/gmtk
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gettext
%if %{with gtk3}
BuildRequires:	gtk+3-devel
%else
BuildRequires:	gtk+2-devel
%endif
BuildRequires:	libtool
BuildRequires:	pulseaudio-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libgmlib.so.0.0.0 libgmtk.so.0.0.0

%description
Library for gnome-mplayer and gecko-mediaplayer.

%package devel
Summary:	Include files for the gmtk
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides the necessary include files to allow you to
develop programs using the gmtk.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	%{!?with_gtk3:--disable-gtk3}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgmlib.so.*.*.*
%ghost %{_libdir}/libgmlib.so.1
%attr(755,root,root) %{_libdir}/libgmtk.so.*.*.*
%ghost %{_libdir}/libgmtk.so.1

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libgmlib.so
%attr(755,root,root) %{_libdir}/libgmtk.so
%{_includedir}/gmtk
%{_pkgconfigdir}/gmlib.pc
%{_pkgconfigdir}/gmtk.pc
