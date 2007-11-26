Name:		configure-trackpoint
Version:	0.2
Release:	%mkrel 3
Summary:	TrackPoint configuration tool
URL:		http://tpctl.sourceforge.net/configure-trackpoint.html
License:	GPL
Group:		System/Configuration/Hardware
Source:		http://prdownloads.sourceforge.net/tpctl/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	ImageMagick desktop-file-utils
%description
Configure-trackpoint is a Gnome TrackPoint configuration tool. It uses the
linux kernel 2.6 TrackPoint driver which at the moment is not in the mainline
kernel but it is available in the multimedia kernel.

%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} << EOF
?package(%{name}): \
command="%{_bindir}/%{name}" \
needs="X11" \
icon="%{name}.png" \
section="Configuration/Hardware" \
title="TrackPoint" \
longtitle="%{summary}" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="SystemSetup" \
  --add-category="Settings;HardwareSettings" \
  --add-category="X-MandrivaLinux-System-Configuration-Hardware" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %{buildroot}/{%{_miconsdir},%{_liconsdir}}
convert -resize 48x48 pixmaps/trackpoint.png %{buildroot}/%{_liconsdir}/%{name}.png
convert -resize 32x32 pixmaps/trackpoint.png %{buildroot}/%{_iconsdir}/%{name}.png
convert -resize 16x16 pixmaps/trackpoint.png %{buildroot}/%{_miconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

consoleperms=/etc/security/console.perms
if ! `grep -q "/proc/trackpoint/" $consoleperms` ; then
        echo "adding entry for /proc/trackpoint/* to your $consoleperms"
        cat >> $consoleperms << EOF

# Added by %{name} to allow user access to /proc/trackpoint
<console>  0600 /proc/trackpoint/* 0600 root
EOF
fi

%postun
%clean_menus

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

%doc AUTHORS

