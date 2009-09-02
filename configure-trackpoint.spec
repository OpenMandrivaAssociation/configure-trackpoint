Name:		configure-trackpoint
Version:	0.6
Release:	%mkrel 4
Summary:	TrackPoint configuration tool
URL:		http://tpctl.sourceforge.net/configure-trackpoint.html
License:	GPL
Group:		System/Configuration/Hardware
Source:		http://prdownloads.sourceforge.net/tpctl/%{name}-%{version}.tar.bz2
Source1:	trackpoint.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	imagemagick desktop-file-utils
Requires:	rpm-helper

%description
Configure-trackpoint is a Gnome TrackPoint configuration tool, which
provides a friendly and descriptive interface to configure various
TrackPoint device's parameters.

%prep
%setup -q

%build
%configure
%make
# the Icon tag shouldn't have an extension, desktop-* complains
sed -i~ -e '/^Icon/s/\.png//' configure-trackpoint.desktop

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
# default provided config is useless and very likely bad (wrong device)
# the user must run the app and save settings to get a working config
cat <<FIN >%{buildroot}/%{_sysconfdir}/trackpoint/trackpoint.conf
# This file is manipulated by the configure-trackpoint program, and sourced
# by %{_initrddir}/trackpoint. Avoid hand editing, it is not guaranteed
# to work as expected.

FIN
rm -rf %{buildroot}/{%{_sysconfdir}/init.d,%{_initrddir}/trackpoint}
cp -p %{SOURCE1} %{buildroot}/%{_initrddir}/trackpoint


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="SystemSetup" \
  --add-category="Settings;HardwareSettings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -resize 48x48 pixmaps/trackpoint.png %{buildroot}/%{_liconsdir}/%{name}.png
convert -resize 32x32 pixmaps/trackpoint.png %{buildroot}/%{_iconsdir}/%{name}.png
convert -resize 16x16 pixmaps/trackpoint.png %{buildroot}/%{_miconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service trackpoint
%if %mdkversion < 200900
%update_menus
%endif

consoleperms=/etc/security/console.perms
if ! `grep -q "/proc/trackpoint/" $consoleperms` ; then
        echo "adding entry for /proc/trackpoint/* to your $consoleperms"
        cat >> $consoleperms << EOF

# Added by %{name} to allow user access to /proc/trackpoint
<console>  0600 /proc/trackpoint/* 0600 root
EOF
fi

%preun
%_preun_service trackpoint

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/*.desktop
%{_initrddir}/trackpoint
%config(noreplace) %{_sysconfdir}/trackpoint/trackpoint.conf

