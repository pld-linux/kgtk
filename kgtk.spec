Summary:	KGtk (Use KDE Dialogs in GTK+ Apps)
Summary(pl):	KGtk - wykorzystywanie okien dialogowych KDE w aplikacjach GTK+
Name:		kgtk
Version:	0.3
Release:	0.2
License:	GPL v2
Group:		Libraries
Source0:	http://home.freeuk.com/cpdrummond/%{name}-%{version}.tar.gz
# Source0-md5:	4502601b7a92895b04f4306b9c0f2f65
URL:		http://www.kde-look.org/content/show.php?content=36077
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an LD_PRELOAD library that allows GTK+ applications to use
KDE's file dialogs when run under KDE. This will only work under KDE,
as the KDE dialog portion is implemented as a KDED module that is
loaded at KDE startup. This creates a UNIX socket through which the
GTK+ apps communicate.

%description -l pl
To jest biblioteka wczytywana przez LD_PRELOAD pozwalaj±ca aplikacjom
GTK+ korzystaæ z okien dialogowych wyboru plików z KDE w czasie
dzia³ania KDE. Dzia³a to tylko pod KDE, jako ¿e czê¶æ dialogowa KDE
jest zaimplementowana jako modu³ KDED wczytywany przy starcie KDE.
Tworzy gniazdo uniksowe, z którym komunikuj± siê aplikacje GTK+.

%prep
%setup -q

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

%{__sed} -i '1s|/bin/bash|/bin/sh|' {gtk,qt}/*-wrapper.sh
cp -f {gtk,qt}/*-wrapper.sh $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_libdir}/libkgtk.so
%{_libdir}/kde3/kded_kdialogd.so
%{_libdir}/kde3/kded_kdialogd.la
%{_libdir}/libkqt.so
%{_libdir}/libkqt.la
%{_datadir}/services/kded/kdialogd.desktop

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
