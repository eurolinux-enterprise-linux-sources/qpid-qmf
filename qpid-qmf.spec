# Spec file for Qpid QMF packages
# svn revision: $Rev$

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%{!?ruby_sitelib: %global ruby_sitelib %(/usr/bin/ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(/usr/bin/ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

# NOTE: no more than one of these flags should be set at the same time!
# RHEL-6 builds (the default) should have all these flags set to 0.
%global fedora              0
%global rhel_4              0
%global rhel_5              0

# LIBRARY VERSIONS
# Update these lib numbers in accordance with library numbering policy
# and best practices.
# http://www.gnu.org/software/libtool/manual/libtool.html#Versioning
#
# Fromat: current[:revision[:age]]
#
# current:  The most recent interface number that this library
#           implements.
# revision: The implementation number of the current interface.
# age:      The difference between the newest and oldest interfaces that
#           this library implements.  In other words, the library
#           implements all the interface numbers in the range from
#           number current - age to current.
#
#  1. Start with version information of ‘0:0:0’ for each libtool
#     library.
#  2. Update the version information only immediately before a public
#     release of your software.  More frequent updates are
#     unnecessary, and only guarantee that the current interface
#     number gets larger faster.
#  3. If the library source code has changed at all since the last
#     update, then increment revision (‘c:r:a’ becomes ‘c:r+1:a’).
#  4. If any interfaces have been added, removed, or changed since the
#     last update, increment current, and set revision to 0.
#  5. If any interfaces have been added since the last public release,
#     then increment age.
#  6. If any interfaces have been removed or changed since the last
#     public release, then set age to 0.

%global QPIDCOMMON_VERSION_INFO             5:0:0
%global QPIDTYPES_VERSION_INFO              3:0:2
%global QPIDBROKER_VERSION_INFO             5:0:0
%global QPIDCLIENT_VERSION_INFO             5:0:0
%global QPIDMESSAGING_VERSION_INFO          4:0:1
%global QMF_VERSION_INFO                    4:0:0
%global QMF2_VERSION_INFO                   1:0:0
%global QMFENGINE_VERSION_INFO              4:0:0
%global QMFCONSOLE_VERSION_INFO             5:0:0
%global RDMAWRAP_VERSION_INFO               5:0:0
%global SSLCOMMON_VERSION_INFO              5:0:0

# Single var with all lib version params (except store) for make
%global LIB_VERSION_MAKE_PARAMS QPIDCOMMON_VERSION_INFO=%{QPIDCOMMON_VERSION_INFO} QPIDTYPES_VERSION_INFO=%{QPIDTYPES_VERSION_INFO} QPIDBROKER_VERSION_INFO=%{QPIDBROKER_VERSION_INFO} QPIDCLIENT_VERSION_INFO=%{QPIDCLIENT_VERSION_INFO} QPIDMESSAGING_VERSION_INFO=%{QPIDMESSAGING_VERSION_INFO} QMF_VERSION_INFO=%{QMF_VERSION_INFO} QMF2_VERSION_INFO=%{QMF2_VERSION_INFO} QMFENGINE_VERSION_INFO=%{QMFENGINE_VERSION_INFO} QMFCONSOLE_VERSION_INFO=%{QMFCONSOLE_VERSION_INFO} RDMAWRAP_VERSION_INFO=%{RDMAWRAP_VERSION_INFO} SSLCOMMON_VERSION_INFO=%{SSLCOMMON_VERSION_INFO}

Name:          qpid-qmf
Version:       0.12
Release:       6%{?dist}
Summary:       The Qpid Management Framework
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://qpid.apache.org
Vendor:        Red Hat, Inc.
Source0:       %{name}-%{version}.tar.gz
Patch0:        unused-result.patch
Patch1:        mutable.patch
Patch2:        abi.patch
Patch3:        patch3.patch
Patch4:        patch4.patch
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if %{rhel_5}
ExclusiveArch: i386 x86_64
%endif

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python-devel
BuildRequires: swig
%if !%{rhel_4}
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
%endif
%if %{rhel_5}
BuildRequires: e2fsprogs-devel
%else
%if !%{rhel_4}
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: libuuid-devel
%endif
%endif

BuildRequires: nss-devel
BuildRequires: nspr-devel


# === Package: qpid-qmf ===

Requires:      qpid-cpp-client = %{version}
Provides:      qmf = %{version}-%{release}
Obsoletes:     qmf < %{version}-%{release}

%description
An extensible management framework layered on Qpid messaging

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libqmf.so.*
%{_libdir}/libqmf2.so.*
%{_libdir}/libqmfengine.so.*
%{_libdir}/libqmfconsole.so.*
%exclude %{_libdir}/*.la


# === Package: qpid-qmf-devel ===
%package devel
Summary:       Header files and tools for developing QMF extensions
Group:         Development/System
Requires:      qpid-qmf = %{version}-%{release}
Requires:      qpid-cpp-client-devel = %{version}
Provides:      qmf-devel = %{version}-%{release}
Obsoletes:     qmf-devel < %{version}-%{release}

%description devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqmf.so
%{_libdir}/libqmf2.so
%{_libdir}/libqmfengine.so
%{_libdir}/libqmfconsole.so
%{_bindir}/qmf-gen
%{python_sitearch}/qmfgen
%{_includedir}/qmf
%{_includedir}/qpid/agent
%{_includedir}/qpid/console


%ifnarch s390 s390x ppc ppc64
# === Package: python-qpid-qmf ===
%package -n python-qpid-qmf
Summary:       Python QMF library for Apache Qpid
Group:         Development/Python
Requires:      qpid-qmf = %{version}-%{release}
Requires:      qpid-cpp-client = %{version}
Requires:      python-qpid = %{version}
Provides:      python-qmf = %{version}-%{release}
Obsoletes:     python-qmf < %{version}-%{release}

%description -n python-qpid-qmf
Python QMF library for Apache Qpid

%files -n python-qpid-qmf
%defattr(-,root,root,-)
%{python_sitearch}/qmf
%{python_sitearch}/cqpid.py*
%{python_sitearch}/_cqpid.so
%{python_sitearch}/qmf.py*
%{python_sitearch}/qmfengine.py*
%{python_sitearch}/_qmfengine.so
%{python_sitearch}/qmf2.py*
%{python_sitearch}/cqmf2.py*
%{python_sitearch}/_cqmf2.so
%exclude %{python_sitelib}/mllib
%exclude %{python_sitelib}/qpid
#%exclude %{python_sitelib}/*.egg-info

%endif

%if !%{rhel_4}
# === Package: ruby-qpid-qmf ===

%ifnarch s390 s390x ppc ppc64
%package -n ruby-qpid-qmf
Summary:       The QPID Management Framework bindings for ruby
Group:         System Environment/Libraries
Requires:      qpid-cpp-client = %{version}
Requires:      qpid-qmf = %{version}-%{release}
Provides:      ruby-qmf = %{version}-%{release}
Obsoletes:     ruby-qmf < %{version}-%{release}

%description -n ruby-qpid-qmf
An extensible managememt framework layered on QPID messaging, bindings
for ruby.

%post -n ruby-qpid-qmf -p /sbin/ldconfig

%postun -n ruby-qpid-qmf -p /sbin/ldconfig

%files -n ruby-qpid-qmf
%defattr(-,root,root,-)
%{ruby_sitelib}/qmf.rb
%{ruby_sitelib}/qmf2.rb
%{ruby_sitearch}/qmfengine.so
%{ruby_sitearch}/cqpid.so
%{ruby_sitearch}/cqmf2.so
%exclude %{ruby_sitearch}/*.la

%endif
%endif
#!%{rhel_4}


# ===

%prep
%setup -q
%patch0 -p0
%patch2 -p2
%patch3 -p2
%patch4 -p2
%if %{rhel_4}
(cd cpp/boost-1.32-support; make apply)
%else
#%patch1 -p0
%endif

%build
%if %{rhel_4}
%global swig_flag "--without-swig"
%else
%global swig_flag "--with-swig"
%endif

(
    cd cpp
    ./bootstrap
    export CXXFLAGS="%{optflags} -DNDEBUG -O3"
    %configure %{swig_flag} --with-sasl --with-ssl \
        --without-help2man --without-cpg --without-libcman --without-xml \
        --without-rdma
    %{__make} %{LIB_VERSION_MAKE_PARAMS}
)

(cd python; %{__python} setup.py build)
(cd extras/qmf; %{__python} setup.py build)

%install
rm -rf %{buildroot}

(cd cpp; make install DESTDIR=%{buildroot})
(cd python; %{__python} setup.py install --skip-build --root %{buildroot})
(cd extras/qmf; %{__python} setup.py install --skip-build --root %{buildroot} --install-purelib %{python_sitearch})

# Move QMF v.2 files from incorrect libtool locations
%if !%{rhel_4}
install -d %{buildroot}%{python_sitelib}
install -d %{buildroot}%{python_sitearch}
install -pm 755 %{buildroot}%{_libdir}/_cqpid.so %{buildroot}%{python_sitearch}
install -pm 755 %{buildroot}%{_libdir}/_qmfengine.so %{buildroot}%{python_sitearch}
install -pm 755 %{buildroot}%{_libdir}/_cqmf2.so %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf/ruby/qmf.rb %{buildroot}%{ruby_sitelib}
install -pm 644 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf2/ruby/qmf2.rb %{buildroot}%{ruby_sitelib}
install -pm 755 %{_builddir}/%{name}-%{version}/cpp/bindings/qpid/ruby/.libs/cqpid.so %{buildroot}%{ruby_sitearch}
install -pm 755 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf/ruby/.libs/qmfengine.so %{buildroot}%{ruby_sitearch}
install -pm 755 %{_builddir}/%{name}-%{version}/cpp/bindings/qmf2/ruby/.libs/cqmf2.so %{buildroot}%{ruby_sitearch}
%endif

shopt -s extglob

rm -fr %{buildroot}%{_libdir}/!(libqmf*|ruby|python*)
rm -fr %{buildroot}%{_localstatedir}
rm -fr %{buildroot}%{_mandir}
rm -fr %{buildroot}%{_bindir}/!(qmf*)
rm -fr %{buildroot}%{_includedir}/qpid/!(agent|console)
rm -fr %{buildroot}%{_includedir}/qmf/org
rm -fr %{buildroot}%{_libexecdir}
rm -fr %{buildroot}%{_sbindir}
rm -fr %{buildroot}%{_sysconfdir}
rm -fr %{buildroot}%{_datadir}
rm -fr %{buildroot}%{python_sitelib}/qpid*.egg-info
rm -fr %{buildroot}%{python_sitearch}/qpid*.egg-info

%ifarch s390 s390x ppc ppc64
rm -fr %{buildroot}%{python_sitearch}/qmf
rm -fr %{buildroot}%{python_sitearch}/cqpid.py*
rm -fr %{buildroot}%{python_sitearch}/_cqpid.so
rm -fr %{buildroot}%{python_sitearch}/qmf.py*
rm -fr %{buildroot}%{python_sitearch}/qmfengine.py*
rm -fr %{buildroot}%{python_sitearch}/_qmfengine.so
rm -fr %{buildroot}%{python_sitearch}/qmf2.py*
rm -fr %{buildroot}%{python_sitearch}/cqmf2.py*
rm -fr %{buildroot}%{python_sitearch}/_cqmf2.so
rm -fr %{buildroot}%{python_sitelib}/mllib
rm -fr %{buildroot}%{python_sitelib}/qpid
rm -fr %{buildroot}%{ruby_sitelib}/qmf.rb
rm -fr %{buildroot}%{ruby_sitelib}/qmf2.rb
rm -fr %{buildroot}%{ruby_sitearch}/qmfengine.so
rm -fr %{buildroot}%{ruby_sitearch}/cqpid.so
rm -fr %{buildroot}%{ruby_sitearch}/cqmf2.so
rm -fr %{buildroot}%{ruby_sitearch}/*.la
%endif

%clean
rm -rf %{buildroot}


%changelog
* Tue Oct 18 2011 Ted Ross <tross@redhat.com> - 0.12-6
- Related:rhbz#743657

* Fri Sep 16 2011 Ted Ross <tross@redhat.com> - 0.12-5
- Related:rhbz#699499 - [RFE] qmfv2 must provide mainloop integration

* Mon Aug 15 2011 Ted Ross <tross@redhat.com> - 0.12-4
- Related:rhbz#681680 - QMF agents wake up several times a second
- Related:rhbz#699499 - [RFE] qmfv2 must provide mainloop integration

* Mon Aug 15 2011 Ted Ross <tross@redhat.com> - 0.12-3
- Related:rhbz#681680 - QMF agents wake up several times a second

* Wed Aug 10 2011 Ted Ross <tross@redhat.com> - 0.12-2
- Related:rhbz#663461 - Enable new architectures
- Remove python-qpid-qmf and ruby-qpid-qmf from ppc and s390 architectures

* Mon Aug  8 2011 Ted Ross <tross@redhat.com> - 0.12-1
- Related:rhbz#706990 - Rebase to Qpid 0.12
- Related:rhbz#663461 - Enable new architectures

* Fri Jun  3 2011 Ted Ross <tross@redhat.com> - 0.10-10
- Sync with the RHEL5 build
- Related:rhbz#710483

* Wed Apr  6 2011 Nuno Santos <nsantos@redhat.com> - 0.10-7
- Fix python multiarch issues

* Wed Mar 30 2011 Nuno Santos <nsantos@redhat.com> - 0.10-5
- Initial version of consolidated, renamed qpid-qmf packages
