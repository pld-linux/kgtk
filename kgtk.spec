Summary:	KGtk (Use KDE Dialogs in Gtk Apps)
Name:		kgtk
Version:	0.3
Release:	0.1
License:	GPL v2
Group:		Libraries
Source0:	http://home.freeuk.com/cpdrummond/%{name}-%{version}.tar.gz
# Source0-md5:	4502601b7a92895b04f4306b9c0f2f65
Patch0:		%{name}-sh.patch
URL:		http://www.kde-look.org/content/show.php?content=36077
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an LD_PRELOAD library that allows Gtk applications to use
KDE's file dialogs when run under KDE. This will only work under KDE,
as the KDE dialog portion is implemented as a KDED module that is
loaded at KDE startup. This creates a UNIX socket through which the
Gtk apps communicate.

%prep
%setup -q
%patch0 -p1

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
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir} \
	kdelnkdir=%{_desktopdir} \

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_pixmapsdir}/*
%{_desktopdir}/*
%{_iconsdir}/*/*/apps/%{name}.png
%{_datadir}/mimelnk/application/*
%{_datadir}/apps/%{name}
