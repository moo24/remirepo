%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.twig-project.org

Name:             php-channel-twig
Version:          1.0
Release:          3%{?dist}
Summary:          Adds %{pear_channel} channel to PEAR

Group:            Development/Libraries
License:          Public Domain
URL:              http://%{pear_channel}
Source0:          http://%{pear_channel}/channel.xml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)

Requires:         php-pear(PEAR)
Requires(post):   %{__pear}
Requires(postun): %{__pear}

Provides:         php-channel(%{pear_channel}) = %{version}

%description
This package adds the %{pear_channel} channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null || :
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete %{pear_channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Sun Jun 09 2012 Remi Collet <RPMS@FamilleCollet.com> 1.0-3
- rebuild for remi repository

* Sat Jun 9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-3
- Changed license from BSD to Public Domain
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Removed cleaning buildroot from %%install section
- Removed %%clean section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2
- %%global instead of %%define
- Removed BuildRoot
- Removed %%defattr from %%files section
- Minor syntax update in %%post section

* Fri Apr 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1
- Initial package