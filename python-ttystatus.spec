#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	ttystatus
Summary:	Progress and status updates on terminals for Python
Name:		python-%{module}
Version:	0.32
Release:	6
License:	GPL v3+
Group:		Libraries/Python
Source0:	http://git.liw.fi/cgi-bin/cgit/cgit.cgi/ttystatus/snapshot/ttystatus-0.32.tar.gz
# Source0-md5:	971cde8afc1bde14bc13091dcd27977e
URL:		http://liw.fi/ttystatus/
BuildRequires:	python-Sphinx
%if %{with python2}
BuildRequires:	python-coverage-test-runner
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
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

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package doc
Summary:	Documentation for %{module}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains the documentation for %{module}, a Python
library providing progress and status updates on terminals.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%{?with_tests:%{__make} -j1 check}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
cd doc
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# drop internal tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/ttystatus/*_tests.py*

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install

# drop internal tests
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/ttystatus/*_tests.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc NEWS README
%{py_sitescriptdir}/ttystatus-%{version}-py*.egg-info
%dir %{py_sitescriptdir}/ttystatus
%{py_sitescriptdir}/ttystatus/*.py[co]
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc NEWS README
%{py3_sitescriptdir}/ttystatus-%{version}-py*.egg-info
%{py3_sitescriptdir}/ttystatus
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/*
