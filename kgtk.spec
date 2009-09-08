#
# TODO:	alternate qt4 build ("Cant compile Qt3/KDE3 at the same time as Qt4/KDE4")
#
%define	_name	KGtk
Summary:	KGtk (Use KDE Dialogs in GTK+ Apps)
Summary(pl.UTF-8):	KGtk - wykorzystywanie okien dialogowych KDE w aplikacjach GTK+
Name:		kgtk
Version:	0.10.1
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://home.freeuk.com/cpdrummond/%{_name}-%{version}.tar.bz2
# Source0-md5:	b456046727f0120734410573d75c47e0
URL:		http://www.kde-look.org/content/show.php?content=36077
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	pkgconfig
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
%setup -q -n %{_name}-%{version}

%build
export kde_htmldir=%{_kdedocdir}
export kde_libs_htmldir=%{_kdedocdir}
export KDEDIR=%{_prefix}
export QTDIR=%{_prefix}
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DKGTK_QT3=true \
	-DKGTK_QT4=false \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif 
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} -C build install \
        DESTDIR=$RPM_BUILD_ROOT \
        kde_htmldir=%{_kdedocdir} \
        kde_libs_htmldir=%{_kdedocdir}

%find_lang %{name} --with-kde --all-name
                        
%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/kgtk
%attr(755,root,root) %{_libdir}/kgtk/libkgtk2.so
%attr(755,root,root) %{_libdir}/kgtk/libkqt3.so
                                        
