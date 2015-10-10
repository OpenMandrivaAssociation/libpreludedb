%define major	7
%define libname	%mklibname preludedb %{major}
%define devname	%mklibname preludedb -d
%define cppmajor		2
%define libcpp			%mklibname preludedbcpp %{cppmajor}

%define _disable_lto 1

Summary:	Provide the framework for easy access to the Prelude database
Name:		libpreludedb
Version:	1.2.6
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.prelude-ids.org/
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
Source4:	libpreludedb-addIndices.sql
Patch1:		libpreludedb-1.2.6-cpp-lib.patch

BuildRequires:	chrpath
BuildRequires:	gtk-doc
BuildRequires:	swig
BuildRequires:	libtool-devel
BuildRequires:	mysql-devel
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libprelude)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)

%description
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n	%{libname}
Summary:	Provide the framework for easy access to the Prelude database
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n     %{libcpp}
Summary:        Provide the framework for easy access to the Prelude database
Group:          System/Libraries

%description -n %{libcpp}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

%package -n	%{devname}
Summary:	Libraries and headers for PreludeDB
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcpp} = %{version}-%{release}
Provides:	preludedb-devel = %{version}-%{release}

%description -n	%{devname}
The PreludeDB Library provides an abstraction layer upon the type
and the format of the database used to store IDMEF alerts. It
allows developers to use the Prelude IDMEF database easily and
efficiently wi thout worrying about SQL, and to access the
database independently of the type/format of the database.

This package contains the development libraries and headers for
PreludeDB.

%package -n	preludedb-tools
Summary:	The interface for %{libname}
Group:		Networking/Other

%description -n	preludedb-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n	python-preludedb
Summary:	Python bindings for PreludeDB
Group:		Development/Python

%description -n	python-preludedb
Provides python bindings for PreludeDB.

%package -n	preludedb-mysql
Summary:	Plugin to use prelude with a MySQL database
Group:		System/Servers

%description -n	preludedb-mysql
This plugin authorise prelude to store alerts into a MySQL
database.

%package -n	preludedb-pgsql
Summary:	Plugin to use prelude with a PostgreSQL database
Group:		System/Servers

%description -n	preludedb-pgsql
This plugin authorise prelude to store alerts into a PostgreSQL
database.

%package -n	preludedb-sqlite3
Summary:	Plugin to use prelude with a SQLite3 database
Group:		System/Servers

%description -n	preludedb-sqlite3
This plugin authorise prelude to store alerts into a SQLite3
database.

%prep
%setup -q
%apply_patches
autoreconf -fiv

%build
export PYTHON=%{__python3}
export CXX=g++
%configure \
	--disable-static \
	--enable-shared \
	--localstatedir=%{_var} \
	--includedir=%{_includedir}/%{name} \
	--with-swig \
	--with-perl-installdirs=vendor \
	--with-python3 \
	--without-python2 \
	--enable-gtk-doc \
	--with-html-dir=%{_docdir}/%{devname}

%make

%install
%makeinstall_std

cp -a %{SOURCE4} %{buildroot}%{_datadir}/%{name}/classic/addIndices.sql

%multiarch_binaries %{buildroot}%{_bindir}/libpreludedb-config

%files -n %{libname}
%doc COPYING ChangeLog HACKING.README LICENSE.README NEWS README
%{_libdir}/libpreludedb.so.%{major}*
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/formats
%dir %{_libdir}/%{name}/plugins/sql
%{_libdir}/%{name}/plugins/formats/classic.so
%{_datadir}/%{name}/classic/addIndices.sql

%files -n %{libcpp}
%{_libdir}/%{name}cpp.so.%{cppmajor}
%{_libdir}/%{name}cpp.so.%{cppmajor}.*

%files -n %{devname}
%doc %{_docdir}/%{devname}
%{multiarch_bindir}/%{name}-config
%{_bindir}/%{name}-config
%{_libdir}/*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/*.hxx
%{_datadir}/aclocal/*.m4

%files -n preludedb-tools
%{_bindir}/preludedb-admin
%{_mandir}/man1/preludedb-admin.1*

%files -n python-preludedb
%{_libdir}/python*/site-packages/*

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

