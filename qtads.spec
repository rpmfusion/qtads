Name:           qtads
Version:        2.1.6
Release:        1%{?dist}
Summary:        Multimedia interpreter for Tads games

# 1) qtads dual licensed under GPLv2+ and TADS license
# 2) project bundles tads2, tads3, and htmltads under TADS license
License:        (GPLv2+ or non-commercial) and non-commercial
URL:            http://qtads.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        qtads.desktop
Patch0:         qtads-disable-updates.patch

BuildRequires:  SDL-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_sound-devel
BuildRequires:  SDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  qt-devel
Requires:       hicolor-icon-theme
Requires:       shared-mime-info
Provides:       bundled(htmltads) = 23
Provides:       bundled(tads2) = 2.5.16
Provides:       bundled(tads3) = 3.1.2
Provides:       bundled(md5-deutsch-c++)
Provides:       bundled(sha2-gladman)

%description
QTads is a cross-platform, multimedia interpreter for Tads games, compatible
with HTML TADS. Both Tads versions in use today (Tads 2 and Tads 3) are
supported.

Tads consists of a programming language and a virtual machine. The system is
geared towards implementing Interactive Fiction (or “Text Adventures”), with
support for multimedia features such as images, music and sounds. If you ever
played an Infocom game like “Zork” or “Trinity”, or the classic game Adventure
by Crowther and Woods, then you know what this is about.


%prep
%setup -q
%patch0 -p1


%build
%qmake_qt4
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/mime/packages
mkdir -p %{buildroot}%{_mandir}/man6
install -p -m 0755 qtads %{buildroot}%{_bindir}/
install -p -m 0644 qtads.6 %{buildroot}%{_mandir}/man6/
for size in 48 72 256; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  install -p -m 0644 qtads_${size}x${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/qtads.png
done
install -p -m 0644 icons/qtads.xml %{buildroot}%{_datadir}/mime/packages/
cp -a icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1} 


%post
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license COPYING HTML_TADS_LICENSE
%doc README
%{_bindir}/qtads
%{_datadir}/applications/qtads.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/mime/packages/qtads.xml
%{_mandir}/man6/qtads.6*


%changelog
* Tue Dec 02 2014 František Dvořák <valtri@civ.zcu.cz> - 2.1.6-1
- Initial package
