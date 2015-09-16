%if 0%{?fedora}
%global with_python3 1
%endif

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%{!?_licensedir: %global license %%doc}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global modname jwt

Name:               python-jwt
Version:            1.4.0
Release:            1%{?dist}
Summary:            JSON Web Token implementation in Python

Group:              Development/Libraries
License:            MIT
URL:                http://pypi.python.org/pypi/pyjwt
Source0:            https://pypi.python.org/packages/source/P/PyJWT/PyJWT-%{version}.tar.gz
BuildArch:          noarch

BuildRequires:      python2-devel
BuildRequires:      python-setuptools
BuildRequires:      python-cryptography
Requires:           python-cryptography

BuildRequires:      pytest
BuildRequires:      python-pytest-cov

%if 0%{?with_python3}
BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
BuildRequires:      python3-cryptography

BuildRequires:      python3-pytest
BuildRequires:      python3-pytest-cov
%endif

%description
A Python implementation of JSON Web Token draft 01. This library provides a
means of representing signed content using JSON data structures, including
claims to be transferred between two parties encoded as digitally signed and
encrypted JSON objects.

%if 0%{?with_python3}
%package -n python3-jwt
Summary:            JSON Web Token implementation in Python
Group:              Development/Libraries
Requires:           python3-cryptography

%description -n python3-jwt
A Python3 implementation of JSON Web Token draft 01. This library provides a
means of representing signed content using JSON data structures, including
claims to be transferred between two parties encoded as digitally signed and
encrypted JSON objects.
%endif

%prep
%setup -q -n PyJWT-%{version}

rm -rf setup.cfg

sed -i '/pytest-runner/d' setup.py

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info
find . -name "*.pyc" -exec rm -rf {} \; || echo;
find . -name "__pycache__" -exec rm -rf {} \; || echo;

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
mv %{buildroot}%{_bindir}/jwt %{buildroot}%{_bindir}/python3-jwt
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
py.test .
%if 0%{?with_python3}
pushd %{py3dir}
py.test-%{python3_version} .
popd
%endif

%files
%doc README.md AUTHORS
%license LICENSE
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/PyJWT-%{version}*
%{_bindir}/jwt

%if 0%{?with_python3}
%files -n python3-jwt
%doc README.md AUTHORS
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/PyJWT-%{version}*
%{_bindir}/python3-jwt
%endif

%changelog
* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 1.4.0-1
- new version

* Wed Jun 17 2015 Ralph Bean <rbean@redhat.com> - 1.3.0-1
- new version
- start running the test suite.

* Fri Mar 27 2015 Ralph Bean <rbean@redhat.com> - 1.0.1-1
- new version

* Thu Mar 19 2015 Ralph Bean <rbean@redhat.com> - 1.0.0-1
- new version

* Fri Feb 20 2015 Ralph Bean <rbean@redhat.com> - 0.4.3-1
- Latest upstream.
- Expand the description as per review feedback.
- Add a comment about the test suite.
- Declare noarch.
- Declare _docdir_fmt

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 0.4.2-1
- initial package for Fedora.
