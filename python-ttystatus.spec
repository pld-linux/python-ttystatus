%define		module	ttystatus
Summary:	Progress and status updates on terminals for Python
Name:		python-%{module}
Version:	0.23
Release:	2
License:	GPL v3+
Group:		Libraries/Python
Source0:	http://code.liw.fi/debian/pool/main/p/python-%{module}/%{name}_%{version}.orig.tar.gz
# Source0-md5:	bfc43748b5a569a0d5e283b2e78814a8
URL:		http://liw.fi/ttystatus/
BuildRequires:	python-Sphinx
BuildRequires:	python-coverage-test-runner
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ttystatus is a Python library for showing progress reporting and
status updates on terminals, for (Unix) command line programs. Output
is automatically adapted to the width of the terminal: truncated if it
does not fit, and re-sized if the terminal size changes.

Output is provided via widgets. Each widgets formats some data into a
suitable form for output. It gets the data either via its initializer,
or from key/value pairs maintained by the master object. The values
are set by the user. Every time a value is updated, widgets get
updated (although the terminal is only updated every so often to give
user time to actually read the output).

%package doc
Summary:	Documentation for %{module}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the documentation for %{module}, a Python
library providing progress and status updates on terminals.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with tests}
# CoverageTestRunner trips up on build directory;
# remove it first
rm -rf build
%{__make} check
%endif

%py_build

# Build documentation
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%py_install

# drop internal tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/ttystatus/*_tests.py*

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%{py_sitescriptdir}/ttystatus-%{version}-py*.egg-info
%dir %{py_sitescriptdir}/ttystatus
%{py_sitescriptdir}/ttystatus/*.py[co]

%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/*
