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
BuildRequires:  libgnutls-devel
BuildRequires:  libltdl-devel
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
Requires:       libltdl-devel
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
