#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	smp		# build the SMP driver
%bcond_with	verbose		# verbose build (V=1)

%define		_corever	8.31
%define		maintainer	alk
%define		origrel	8

%define		_rel	1

Summary:	Kernel module for Lucent modems
Summary(de.UTF-8):   Kernmodul für Lucent-Modems
Summary(pl.UTF-8):   Moduł jądra dla modemów Lucent
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
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.118
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

%package -n kernel-char-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de.UTF-8):   Kernmodul für Lucent-Modems
Summary(pl.UTF-8):   Moduł jądra dla modemów Lucent
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-9
Obsoletes:	kernel-net-ltmodem
Obsoletes:	ltmodem
Conflicts:	ppp < 2.4.0

%description -n kernel-char-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-char-ltmodem -l de.UTF-8
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -n kernel-char-ltmodem -l pl.UTF-8
ltmodem jest modułem jądra obsługującym modemy oparte na układach
Lucent. Modemy te udostępniane są jako urządzenie /dev/ttyLT0.

%package -n kernel-smp-char-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de.UTF-8):   Kernmodul für Lucent-Modems
Summary(pl.UTF-8):   Moduł jądra dla modemów Lucent
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-9
Obsoletes:	kernel-smp-net-ltmodem
Obsoletes:	ltmodem
Conflicts:	ppp < 2.4.0

%description -n kernel-smp-char-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-smp-char-ltmodem -l de.UTF-8
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -n kernel-smp-char-ltmodem -l pl.UTF-8
ltmodem jest modułem jądra obsługującym modemy oparte na układach
Lucent. Modemy te udostępniane są jako urządzenie /dev/ttyLT0.

%prep
%setup -q -n %{name}-2.6-%{maintainer}-%{origrel}

# to make sure that the right version is used
if [ \! -f ltmdmobj.o-%{_corever} ]; then exit 1; fi

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -f *.o
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	ln -s ltmdmobj.o-%{_corever} ltmdmobj.o
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	for i in ltmodem ltserial; do
		mv $i{,-$cfg}.ko
	done
done


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
%if %{with smp}
for mod in *smp.ko; do
	nmod=$(echo "$mod" | sed -e 's#-smp##g')
	install $mod $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/$nmod
done
%endif

for mod in *up.ko; do
	nmod=$(echo "$mod" | sed -e 's#-up##g')
	install $mod $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$nmod
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-char-ltmodem
%depmod %{_kernel_ver}

%postun	-n kernel-char-ltmodem
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-ltmodem
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-char-ltmodem
%depmod %{_kernel_ver}smp

%files -n kernel-char-ltmodem
%defattr(644,root,root,755)
%doc docs/*
/lib/modules/%{_kernel_ver}/*/*

%if %{with smp}
%files -n kernel-smp-char-ltmodem
%defattr(644,root,root,755)
%doc docs/*
/lib/modules/%{_kernel_ver}smp/*/*
%endif
