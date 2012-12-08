%define major                   0
%define libname                 %mklibname preludedb %{major}
%define libnamedevel            %mklibname preludedb -d
%define libnamestaticdevel      %mklibname preludedb -d -s

Name:           libpreludedb
Version:        1.0.1
Release:        %mkrel 0.0.p1.1
Summary:        Provide the framework for easy access to the Prelude database
License:        GPLv2+
Group:          System/Libraries
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/%{name}-%{version}p1.tar.gz
Source4:        libpreludedb-addIndices.sql
BuildRequires:  chrpath
BuildRequires:  gtk-doc
BuildRequires:  gnutls-devel
BuildRequires:  libtool-devel
BuildRequires:  mysql-devel
BuildRequires:  openssl-devel
BuildRequires:  perl-devel
BuildRequires:  postgresql-devel
BuildRequires:  prelude-devel
BuildRequires:  python-devel
BuildRequires:  sqlite3-devel
BuildRequires:  swig
BuildRequires:  zlib-devel

%description
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n	%{libname}
Summary:        Provide the framework for easy access to the Prelude database
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{libname}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n %{libnamedevel}
Summary:        Libraries and headers for PreludeDB
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       openssl-devel
Requires:       libtool-devel
Provides:       preludedb-devel = %{version}-%{release}
Provides:       %{_lib}preludedb-devel = %{version}-%{release}
Provides:       preludedb-devel = %{version}-%{release}
Obsoletes:	%mklibname -d preludedb 0

%description -n %{libnamedevel}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

This package contains the development libraries and headers for
PreludeDB.

%package -n preludedb-tools
Summary:        The interface for %{libname}
Group:          Networking/Other
Requires:       %{libname} = %{version}-%{release}

%description -n preludedb-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n python-preludedb
Summary:        Python bindings for PreludeDB
Group:          Development/Python
Requires:       %{libname} = %{version}-%{release}

%description -n python-preludedb
Provides python bindings for PreludeDB.

%package -n perl-preludedb
Summary:        Perl bindings for PreludeDB
Group:          Development/Perl
Requires:       %{libname} = %{version}-%{release}

%description -n perl-preludedb
Provides perl bindings for PreludeDB.

%package -n preludedb-mysql
Summary:        Plugin to use prelude with a MySQL database
Group:          System/Servers
Requires:       %{libname} = %{version}-%{release}
Obsoletes:      prelude-manager-mysql-plugin < %{version}-%{release}
Provides:       prelude-manager-mysql-plugin = %{version}-%{release}

%description -n preludedb-mysql
This plugin authorise prelude to store alerts into a MySQL
database.

%package -n preludedb-pgsql
Summary:        Plugin to use prelude with a PostgreSQL database
Group:          System/Servers
Requires:       %{libname} = %{version}-%{release}
Obsoletes:      prelude-manager-pgsql-plugin < %{version}-%{release}
Provides:       prelude-manager-pgsql-plugin = %{version}-%{release}

%description -n preludedb-pgsql
This plugin authorise prelude to store alerts into a PostgreSQL
database.

%package -n preludedb-sqlite3
Summary:        Plugin to use prelude with a SQLite3 database
Group:          System/Servers
Requires:       %{libname} = %{version}-%{release}

%description -n preludedb-sqlite3
This plugin authorise prelude to store alerts into a SQLite3
database.

%prep
%setup -q -n %{name}-%{version}p1

%build
%configure2_5x \
    --disable-rpath \
    --disable-static \
    --enable-shared \
    --localstatedir=%{_var} \
    --includedir=%{_includedir}/%{name} \
    --with-swig \
    --with-perl-installdirs=vendor \
    --with-python \
    --enable-gtk-doc \
    --with-html-dir=%{_docdir}/%{libnamedevel}
%make

%install
%{__rm} -rf %{buildroot}

%makeinstall_std
%makeinstall_std -C bindings/perl

%{__cp} -a %{SOURCE4} %{buildroot}%{_datadir}/%{name}/classic/addIndices.sql

%multiarch_binaries %{buildroot}%{_bindir}/libpreludedb-config

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a
rm -f %{buildroot}%{_libdir}/%{name}/plugins/formats/*.*a
rm -f %{buildroot}%{_libdir}/%{name}/plugins/sql/*.*a

%files -n %{libname}
%doc COPYING ChangeLog HACKING.README LICENSE.README NEWS README
%{_libdir}/lib*.so.*
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/formats
%dir %{_libdir}/%{name}/plugins/sql
%{_libdir}/%{name}/plugins/formats/classic.so
%{_datadir}/%{name}/classic/addIndices.sql

%files -n %{libnamedevel}
%doc %{_docdir}/%{libnamedevel}
%{multiarch_bindir}/%{name}-config
%{_bindir}/%{name}-config
%{_libdir}/*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_datadir}/aclocal/*.m4

%files -n preludedb-tools
%{_bindir}/preludedb-admin
%{_mandir}/man1/preludedb-admin.1*

%files -n python-preludedb
%{_libdir}/python*/site-packages/*

%files -n perl-preludedb
%{perl_vendorlib}/*/auto/PreludeDB/PreludeDB.so
%{perl_vendorlib}/*/PreludeDB.pm

%files -n preludedb-mysql
%{_libdir}/%{name}/plugins/sql/mysql.so
%attr(0755,root,root) %{_datadir}/%{name}/classic/mysql2sqlite.sh
%attr(0755,root,root) %{_datadir}/%{name}/classic/mysql2pgsql.sh
%{_datadir}/%{name}/classic/mysql*.sql

%files -n preludedb-pgsql
%{_libdir}/%{name}/plugins/sql/pgsql.so
%{_datadir}/%{name}/classic/pgsql*.sql

%files -n preludedb-sqlite3
%{_libdir}/%{name}/plugins/sql/sqlite3.so
%{_datadir}/%{name}/classic/sqlite*.sql


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2011.0
+ Revision: 662408
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6
+ Revision: 645750
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2011.0
+ Revision: 627000
- rebuilt against mysql-5.5.8 libs, again

* Mon Dec 27 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2011.0
+ Revision: 625421
- rebuilt against mysql-5.5.8 libs

* Mon Nov 01 2010 Funda Wang <fwang@mandriva.org> 1.0.0-3mdv2011.0
+ Revision: 591329
- rebuild for py 2.7

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 1.0.0-2mdv2011.0
+ Revision: 564325
- rebuild for perl 5.12.1

* Sun Apr 25 2010 Funda Wang <fwang@mandriva.org> 1.0.0-1mdv2010.1
+ Revision: 538657
- New version 1.0.0
- disable static libs

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.15.1-6mdv2010.1
+ Revision: 507032
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.9.15.1-5mdv2010.0
+ Revision: 425691
- rebuild

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 0.9.15.1-4mdv2009.1
+ Revision: 319811
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - use lowercase mysql-devel

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.15.1-3mdv2009.1
+ Revision: 311201
- rebuilt against mysql-5.1.30 libs

* Fri Oct 17 2008 Funda Wang <fwang@mandriva.org> 0.9.15.1-2mdv2009.1
+ Revision: 294712
- rebuild for package loss

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 0.9.15.1-1mdv2009.1
+ Revision: 292806
- New version 0.9.15.1

* Thu Aug 28 2008 Funda Wang <fwang@mandriva.org> 0.9.15-1mdv2009.0
+ Revision: 276781
- add missing file
- New version 0.9.15

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.14.1-5mdv2009.0
+ Revision: 229889
- drop the pgsql headers patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 0.9.14.1-3mdv2008.1
+ Revision: 155663
- rebuild for new perl

* Mon Jan 21 2008 Funda Wang <fwang@mandriva.org> 0.9.14.1-2mdv2008.1
+ Revision: 155599
- rebuild against latest gnutls

* Fri Jan 04 2008 Jérôme Soyer <saispo@mandriva.org> 0.9.14.1-1mdv2008.1
+ Revision: 144990
- New release

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 05 2007 Funda Wang <fwang@mandriva.org> 0.9.13-3mdv2008.0
+ Revision: 80181
- fix BR
- obsoletes old devel package

* Mon Aug 20 2007 David Walluck <walluck@mandriva.org> 0.9.13-2mdv2008.0
+ Revision: 68089
- fix some typos
- fix html-dir

* Mon Aug 20 2007 David Walluck <walluck@mandriva.org> 0.9.13-1mdv2008.0
+ Revision: 68081
- regenerate configure in %%prep
- 0.9.13
- new lib policy
- add static lib package
- remove numeric_to_bigint patch (fixed upstream)
- no need to regenerate configure
- more strict directory permissions
- move %%{_datadir}/%%{name}/classic out of lib package (still does not fix multi-owership problem)
- change html-dir from %%{_datadir}/doc/%%{name}-devel-%%{version} to %%{_docdir}/%%{name}-devel (still not ideal)

* Tue Aug 07 2007 David Walluck <walluck@mandriva.org> 0.9.12-1mdv2008.0
+ Revision: 59751
- 0.9.12

* Wed May 16 2007 David Walluck <walluck@mandriva.org> 0.9.11.3-3mdv2008.0
+ Revision: 27258
- add patch from <https://trac.prelude-ids.org/ticket/225>

* Sat May 12 2007 David Walluck <walluck@mandriva.org> 0.9.11.3-2mdv2008.0
+ Revision: 26470
- add additional SQL file


* Fri Feb 09 2007 David Walluck <walluck@mandriva.org> 0.9.11.3-1mdv2007.0
+ Revision: 118271
- 0.9.11.3

* Sun Jan 07 2007 David Walluck <walluck@mandriva.org> 0.9.11.1-1mdv2007.1
+ Revision: 105075
- 0.9.11.1

* Thu Dec 21 2006 David Walluck <walluck@mandriva.org> 0.9.11-2mdv2007.1
+ Revision: 100901
- fix some macros

* Thu Dec 21 2006 David Walluck <walluck@mandriva.org> 0.9.11-1mdv2007.1
+ Revision: 100893
- 9.11-1

* Thu Oct 19 2006 David Walluck <walluck@mandriva.org> 0.9.10-2mdv2007.0
+ Revision: 71044
- fix build
- 0.9.10
- Import libpreludedb

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.8.1-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Tue Jul 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.8.1-1mdv2007.0
- 0.9.8.1

* Fri Jun 16 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-1mdv2007.0
- 0.9.8 (Major bugfixes)

* Fri Mar 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.7.1-1mdk
- 0.9.7.1 (Minor bugfixes)

* Thu Mar 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdk
- 0.9.6 (Minor bugfixes)
- rediffed P0

* Mon Mar 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.5.1-1mdk
- 0.9.5.1

* Wed Feb 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-1mdk
- 0.9.5 (Major bugfixes)
- added P0 to make it find the postgresql headers

* Wed Feb 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.4-1mdk
- 0.9.4 (Major bugfixes)

* Mon Jan 16 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-1mdk
- 0.9.3
- added the sqlite sub package
- fix autofoo

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdk
- initial Mandriva package

