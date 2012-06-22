%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
Name:      mod_gnutls
Version:   0.5.10
Release:   6%{?dist}
Summary:   GnuTLS module for the Apache HTTP server
Group:     System Environment/Daemons
License:   ASL 2.0
URL:       http://modgnutls.sourceforge.net/
Source0:   http://modgnutls.sourceforge.net/downloads/%{name}-%{version}.tar.bz2
Source1:   mod_gnutls.conf
Patch0:    mod_gnutls_apr_memcache_m4_dirty.patch
Patch1:    mod_gnutls-0.5.10-httpd24.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: gnutls-devel, gnutls-utils, httpd-devel, apr-util-devel >= 1.3, libtool, autoconf, automake
Requires:  apr-util >= 1.3, gnutls-utils, httpd-mmn = %{_httpd_mmn}

%description
mod_gnutls uses the GnuTLS library to provide SSL 3.0, TLS 1.0 and TLS 1.1
encryption for Apache HTTPD.  It is similar to mod_ssl in purpose, but does
not use OpenSSL.  A primary benefit of using this module is the ability to
configure multiple SSL certificates for a single IP-address/port combination
(useful for securing virtual hosts).
    
Features
    * Support for SSL 3.0, TLS 1.0 and TLS 1.1.
    * Support for client certificates.
    * Support for RFC 5081 OpenPGP certificate authentication.
    * Support for Server Name Indication.
    * Distributed SSL Session Cache via Memcached
    * Local SSL Session Cache using DBM
    * Sets enviromental vars for scripts (compatible with mod_ssl vars)
    * Small and focused code base:
         Lines of code in mod_gnutls: 3,593
         Lines of code in mod_ssl: 15,324

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .httpd24
cp %{SOURCE1} .

%build
rm -f configure
export APR_MEMCACHE_LIBS="`apu-1-config --link-ld`"
export APR_MEMCACHE_CFLAGS="`apu-1-config --includes`"
autoreconf -f -i

rm -rf autom4te.cache

%configure --disable-srp %{?_httpd_apxs:--with-apxs=%{_httpd_apxs}}
%{__make} %{?_smp_mflags}

%check
%{__make} check

%install
rm -rf %{buildroot}
%{__install} -m 755 -D src/.libs/libmod_gnutls.so %{buildroot}%{_libdir}/httpd/modules/mod_gnutls.so
%{__install} -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/mod_gnutls.conf

%clean
rm -rf %{buildroot}

%pre
rm -fr %{_localstatedir}/cache/mod_gnutls

%files
%defattr(-,root,root,-)
%doc README NEWS NOTICE LICENSE README.ENV
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_gnutls.conf

%changelog
* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.5.10-6
- rebuild for remi repo and httpd 2.4

* Thu Mar 29 2012 Joe Orton <jorton@redhat.com> - 0.5.10-6
- fix build w/httpd 2.4

* Tue Mar 27 2012 Jiri Kastner <jkastner@redhat.com> - 0.5.10-5
- httpd 2.4 rebuild

* Mon Mar 19 2012 Jiri Kastner <jkastner@redhat.com> - 0.5.10-4
- removed httpd require

* Wed Mar 14 2012 Jiri Kastner <jkastner@redhat.com> - 0.5.10-3
- added dependency for httpd-mmn

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 27 2011 Jiri Kastner <jkastner@redhat.com> - 0.5.10-1
- apr_memcache.m4 modified for correct cheking of apr_memcache in apr-util
- removed /var/cache/mod_gnutls from 'files' and 'install' stanzas
- added 'pre' stanza for removal of old cache
- update to 0.5.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 17 2009 Erick Calder <rpm@arix.com> - 0.5.5-5
- removed use of define {ooo}

* Thu Sep 17 2009 Erick Calder <rpm@arix.com> - 0.5.5-4
- dependency generator missed need for httpd.  added by hand.
- abstracted Source0:

* Tue Sep 15 2009 Erick Calder <rpm@arix.com> - 0.5.5-3
- mention of SRP removed from description of package
- added httpd-devel to build requires
- fixed license (harmonized with httpd)

* Tue Sep 15 2009 Erick Calder <rpm@arix.com> - 0.5.5-2
- Added BuildRequires
- removed comments stating the specfile was generated by cpan2rpm
- added BuildRoot
- added install clean

* Fri Sep 11 2009 Erick Calder <rpm@arix.com> - 0.5.5-2
- Initial build
