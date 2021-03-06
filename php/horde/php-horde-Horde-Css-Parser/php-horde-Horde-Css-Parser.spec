# spec file for php-horde-Horde-Css-Parser
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Css_Parser
%global pear_channel pear.horde.org


Name:           php-horde-Horde-Css-Parser
Version:        1.0.3
Release:        1%{?dist}
Summary:        Horde CSS Parser

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.0
Requires:       php-mbstring
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-PHP-CSS-Parser >= 5.0.8
# From phpcompatinfo report for 1.0.2
Requires:       php-iconv
Requires:       php-pcre

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package provides access to the Sabberworm CSS Parser from within the
Horde framework.


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml

sed -e '/Sabberworm\/CSS/d' \
    -e '/EXPAT_LICENSE/d' \
    -i %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Css


%changelog
* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (no change)

* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 for PHP-CSS-Parser 5.0.8

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- use system php-PHP-CSS-Parser

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, with bundled lib (need to be cleaned)
