%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Crypt_Blowfish
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Crypt-Blowfish
Version:        1.0.2
Release:        1%{?dist}
Summary:        Blowfish Encryption Library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-hash
BuildRequires:  php-mcrypt
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-common >= 5.3.0
Requires:       php-hash
Requires:       php-mcrypt
Requires:       php-openssl
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Support) >= 3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Provides blowfish encryption/decryption for PHP string data.

%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit\
    -d include_path=%{buildroot}%{pear_phpdir}:.:%{pear_phpdir} \
    -d date.timezone=UTC \
%if 0%{?rhel} == 5
    . || exit 0
%else
    .
%endif


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
# dir also owned by Horde_Crypt which is not required
%dir %{pear_phpdir}/Horde/Crypt
%{pear_phpdir}/Horde/Crypt/Blowfish
%{pear_phpdir}/Horde/Crypt/Blowfish.php
%{pear_testdir}/%{pear_name}


%changelog
* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- Update to 1.0.2 for remi repo
- skip test in EL-5

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 for remi repo (no change)

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial package
