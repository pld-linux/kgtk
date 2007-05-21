Summary:	KGtk (Use KDE Dialogs in GTK+ Apps)
Summary(pl.UTF-8):	KGtk - wykorzystywanie okien dialogowych KDE w aplikacjach GTK+
Name:		kgtk
Version:	0.7
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://home.freeuk.com/cpdrummond/%{name}-%{version}.tar.gz
# Source0-md5:	2cde8a09508773cf2f9028912be4fbbe
Patch0:		kde-ac260.patch
Patch1:		%{name}-am110.patch
URL:		http://www.kde-look.org/content/show.php?content=36077
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an LD_PRELOAD library that allows GTK+ applications to use
KDE's file dialogs when run under KDE. This will only work under KDE,
as the KDE dialog portion is implemented as a KDED module that is
loaded at KDE startup. This creates a UNIX socket through which the
GTK+ apps communicate.

%description -l pl.UTF-8
To jest biblioteka wczytywana przez LD_PRELOAD pozwalająca aplikacjom
GTK+ korzystać z okien dialogowych wyboru plików z KDE w czasie
działania KDE. Działa to tylko pod KDE, jako że część dialogowa KDE
jest zaimplementowana jako moduł KDED wczytywany przy starcie KDE.
Tworzy gniazdo uniksowe, z którym komunikują się aplikacje GTK+.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--with-qt-libraries=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__sed} -i '1s|/bin/bash|/bin/sh|' {gtk,qt}/*-wrapper.sh

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	wrapperdir=%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/libkgtk.so
%attr(755,root,root) %{_libdir}/kde3/kded_kdialogd.so
%{_libdir}/kde3/kded_kdialogd.la
%attr(755,root,root) %{_libdir}/libkqt.so
%{_libdir}/libkqt.la
%{_libdir}/libkgtk.la
%{_datadir}/services/kded/kdialogd.desktop
