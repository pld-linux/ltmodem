#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	smp		# build the SMP driver

%define		_corever	8.31
%define		maintainer	alk
%define		origrel	7a

%define		_rel	1

Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	%{_corever}.%{maintainer}.%{origrel}
Release:	%{_rel}
License:	unknown
Group:		Base/Kernel
Source0:	http://linmodems.technion.ac.il/packages/ltmodem/kernel-2.6/%{name}-2.6-%{maintainer}-%{origrel}.tar.gz
# NoSource0-md5:	d787ab30c73e4e0f7c9485bfb8a1c26d
NoSource:	0
URL:		http://linmodems.technion.ac.il/resources.html#lucent
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.0}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -l de
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -l pl
ltmodem jest modu³em j±dra obs³uguj±cym modemy oparte na uk³adach
Lucent. Modemy te udostêpniane s± jako urz±dzenie /dev/ttyLT0.

%package -n kernel-char-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-9
Conflicts:	ppp < 2.4.0
Obsoletes:	ltmodem
Obsoletes:	kernel-net-ltmodem

%description -n kernel-char-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-char-ltmodem -l de
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -n kernel-char-ltmodem -l pl
ltmodem jest modu³em j±dra obs³uguj±cym modemy oparte na uk³adach
Lucent. Modemy te udostêpniane s± jako urz±dzenie /dev/ttyLT0.

%package -n kernel-smp-char-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-9
Conflicts:	ppp < 2.4.0
Obsoletes:	ltmodem
Obsoletes:	kernel-smp-net-ltmodem

%description -n kernel-smp-char-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-smp-char-ltmodem -l de
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Gerät gewährt.

%description -n kernel-smp-char-ltmodem -l pl
ltmodem jest modu³em j±dra obs³uguj±cym modemy oparte na uk³adach
Lucent. Modemy te udostêpniane s± jako urz±dzenie /dev/ttyLT0.

%prep
%setup -q -n %{name}-2.6-%{maintainer}-%{origrel}

# to make sure that the right version is used
if [ \! -f ltmdmobj.o-%{_corever} ]; then exit 1; fi

%build
for cfg in up %{?with_smp:smp}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d modules
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
	
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD V=1
	for mod in *.ko; do
		mod=$(echo "$mod" | sed -e 's#\.ko##g')
		mv -v $mod.ko modules/$mod-$cfg.ko
	done
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
cd modules
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
