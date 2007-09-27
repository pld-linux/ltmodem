#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_with	verbose		# verbose build (V=1)

%define		_corever	8.31
%define		maintainer	alk
%define		origrel		8

%define		_rel	0.1

Summary:	Kernel module for Lucent modems
Summary(de.UTF-8):	Kernmodul für Lucent-Modems
Summary(pl.UTF-8):	Moduł jądra dla modemów Lucent
Name:		ltmodem
Version:	%{_corever}.%{maintainer}.%{origrel}
Release:	%{_rel}
License:	unknown
Group:		Base/Kernel
Source0:	http://linmodems.technion.ac.il/packages/ltmodem/kernel-2.6/%{name}-2.6-%{maintainer}-%{origrel}.tar.bz2
# NoSource0-md5:	0f7df8d31cf662a4afaa378fa5bf790b
NoSource:	0
URL:		http://linmodems.technion.ac.il/resources.html#lucent
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
ExclusiveArch:	%{ix86}
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -l de.UTF-8
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -l pl.UTF-8
ltmodem jest modułem jądra obsługującym modemy oparte na układach
Lucent. Modemy te udostępniane są jako urządzenie /dev/ttyLT0.

%package -n kernel%{_alt_kernel}-char-%{name}
Summary:	Kernel module for Lucent modems
Summary(de.UTF-8):	Kernmodul für Lucent-Modems
Summary(pl.UTF-8):	Moduł jądra dla modemów Lucent
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-9
Obsoletes:	kernel-net-ltmodem
Obsoletes:	ltmodem
Conflicts:	ppp < 2.4.0

%description -n kernel%{_alt_kernel}-char-%{name}
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel%{_alt_kernel}-char-%{name} -l de.UTF-8
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -n kernel%{_alt_kernel}-char-%{name} -l pl.UTF-8
ltmodem jest modułem jądra obsługującym modemy oparte na układach
Lucent. Modemy te udostępniane są jako urządzenie /dev/ttyLT0.

%prep
%setup -q -n %{name}-2.6-%{maintainer}-%{origrel}

# to make sure that the right version is used
if [ \! -f ltmdmobj.o-%{_corever} ]; then exit 1; fi

%build
%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{name} -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-char-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-%{name}
%depmod %{_kernel_ver}

%if %{with dist_kernel}
%files -n kernel%{_alt_kernel}-char-%{name}
%defattr(644,root,root,755)
%doc docs/*
/lib/modules/%{_kernel_ver}/misc/*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf
%endif
