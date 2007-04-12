%define major          0
%define libname        %mklibname preludedb %{major}

Summary:        Provide the framework for easy access to the Prelude database
Name:           libpreludedb
Version:        0.9.11.3
Release:        %mkrel 1
License:        GPL
Group:          System/Libraries
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
Source1:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz.sig
Source2:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz.md5
Source3:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.txt
Patch0:         libpreludedb-0.9.6-postgresql_headers.diff
BuildRequires:  automake1.8
BuildRequires:  autoconf2.5
BuildRequires:  chrpath
BuildRequires:  openssl-devel
BuildRequires:  libltdl-devel
BuildRequires:  libgnutls-devel
BuildRequires:  zlib-devel
BuildRequires:  libprelude-devel
BuildRequires:  MySQL-devel
BuildRequires:  postgresql-devel
BuildRequires:  python-devel
BuildRequires:  perl-devel
BuildRequires:  gtk-doc
BuildRequires:  sqlite3-devel
BuildRequires:  swig-devel
%if %mdkversion >= 1020
BuildRequires:  multiarch-utils => 1.0.3
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n %{libname}
Summary:        Provide the framework for easy access to the Prelude database
Group:          System/Libraries
Provides:       %{name} = %{version}

%description -n %{libname}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n %{libname}-devel
Summary:        Libraries and headers for PreludeDB
Group:          Development/C
Requires:       %{libname} = %{version}
Requires:       openssl-devel
Requires:       libltdl-devel
Provides:       libpreludedb-devel = %{version}
Provides:       %{_lib}preludedb-devel = %{version}
Provides:       preludedb-devel = %{version}

%description -n %{libname}-devel
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
Requires:       %{libname} = %{version}

%description -n preludedb-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n python-preludedb
Summary:        Python bindings for PreludeDB
Group:          Development/Python
Requires:       %{libname} = %{version}

%description -n python-preludedb
Provides python bindings for PreludeDB.

%package -n perl-preludedb
Summary:        Perl bindings for PreludeDB
Group:          Development/Perl
Requires:       %{libname} = %{version}

%description -n perl-preludedb
Provides perl bindings for PreludeDB.

%package -n preludedb-mysql
Summary:        Plugin to use prelude with a MySQL database
Group:          System/Servers
Requires:       %{libname} = %{version}
Provides:       prelude-manager-mysql-plugin
Obsoletes:       prelude-manager-mysql-plugin

%description -n preludedb-mysql
This plugin authorise prelude to store alerts into a MySQL
database.

%package -n preludedb-pgsql
Summary:        Plugin to use prelude with a PostgreSQL database
Group:          System/Servers
Requires:       %{libname} = %{version}
Provides:       prelude-manager-pgsql-plugin
Obsoletes:      prelude-manager-pgsql-plugin

%description -n preludedb-pgsql
This plugin authorise prelude to store alerts into a PostgreSQL
database.

%package -n preludedb-sqlite3
Summary:        Plugin to use prelude with a SQLite3 database
Group:          System/Servers
Requires:       %{libname} = %{version}

%description -n preludedb-sqlite3
This plugin authorise prelude to store alerts into a SQLite3
database.

%prep
%setup -q
%patch0 -p0
%{__perl} -pi -e "s|/lib/|/%{_lib}/|g" configure.in

%build
%{__rm} -f configure
%{__libtoolize} --copy --force; aclocal-1.8 -I m4 -I libmissing/m4; automake-1.8 --add-missing --copy --foreign; %{__autoconf}

%{configure2_5x} \
    --enable-static \
    --enable-shared \
    --localstatedir=%{_var} \
    --includedir=%{_includedir}/%{name} \
    --with-libprelude-prefix=%{_prefix} \
    --with-mysql=%{_prefix} \
    --with-pgsql=%{_prefix} \
    --with-sqlite3=%{_prefix} \
    --with-swig \
    --with-perl-installdirs=vendor \
    --with-python \
    --enable-gtk-doc \
    --with-html-dir=%{_datadir}/doc/%{name}-devel-%{version}

%{make}

%install
%{__rm} -rf %{buildroot}

%{makeinstall_std}
%{makeinstall_std} -C bindings/perl

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libpreludedb.so.0.?.? \
                      %{buildroot}%{_libdir}/libpreludedb/plugins/formats/classic.so \
                      %{buildroot}%{_libdir}/libpreludedb/plugins/sql/mysql.so \
                      %{buildroot}%{_libdir}/libpreludedb/plugins/sql/pgsql.so \
                      %{buildroot}%{_libdir}/libpreludedb/plugins/sql/sqlite3.so

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/libpreludedb-config
%endif

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING ChangeLog HACKING.README LICENSE.README NEWS README
%{_libdir}/lib*.so.*
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/formats
%dir %{_libdir}/%{name}/plugins/sql
%{_libdir}/%{name}/plugins/formats/classic.so
%dir %{_datadir}/%{name}/classic

%files -n %{libname}-devel
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-devel-%{version}
%if %mdkversion >= 1020
%{multiarch_bindir}/%{name}-config
%endif
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_datadir}/aclocal/*.m4
%{_libdir}/%{name}/plugins/formats/*.a
%{_libdir}/%{name}/plugins/formats/*.la
%{_libdir}/%{name}/plugins/sql/*.la
%{_libdir}/%{name}/plugins/sql/*.a

%files -n preludedb-tools
%defattr(-,root,root)
%doc COPYING ChangeLog HACKING.README LICENSE.README NEWS README
%{_bindir}/preludedb-admin

%files -n python-preludedb
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*

%files -n perl-preludedb
%defattr(-,root,root)
%{perl_vendorlib}/*/auto/PreludeDB/PreludeDB.so
%{perl_vendorlib}/*/PreludeDB.pm

%files -n preludedb-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/sql/mysql.so
%attr(0755,root,root) %{_datadir}/%{name}/classic/mysql2sqlite.sh
%attr(0755,root,root) %{_datadir}/%{name}/classic/mysql2pgsql.sh
%{_datadir}/%{name}/classic/*.sql

%files -n preludedb-pgsql
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/sql/pgsql.so
%{_datadir}/%{name}/classic/pgsql*

%files -n preludedb-sqlite3
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/sql/sqlite3.so
%{_datadir}/%{name}/classic/sqlite*


