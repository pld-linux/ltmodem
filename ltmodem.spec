#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	smp		# build the SMP driver

%define		_rel	1

Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	8.31a9
Release:	%{_rel}
License:	unknown
Group:		Base/Kernel
Source0:	http://linmodems.technion.ac.il/packages/ltmodem/archive/source/%{name}-%{version}.tar.gz
# NoSource0-md5:	bd0e54ddb2c7037b644b9c6cb6bce9ea
NoSource:	0
URL:		http://linmodems.technion.ac.il/Ltmodem.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.3.0}
BuildRequires:	rpmbuild(macros) >= 1.118
ExclusiveArch:	%{ix86}
ExclusiveOS:	Linux

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
Requires(post,postun):	modutils >= 2.4.6-3
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
Requires(post,postun):	modutils >= 2.4.6-3
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
%setup -q
tar xzf source.tar.gz

%build
cd source
%{__autoconf}

CFLAGS="%{rpmcflags} -I%{_kernelsrcdir}/include"
%configure \
	--with-force=yes \
	--with-kernel=%{_kernelsrcdir}
for cfg in up %{?with_smp:smp}; do
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD V=1
	mkdir $cfg
	mv lt_*.o *.ko $cfg
done

%install
rm -rf $RPM_BUILD_ROOT
install -dD $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install source/up/*.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%if %{with smp}
install source/smp/*.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif

rm -rf DOCs/Installers

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
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}
/lib/modules/%{_kernel_ver}/*/*

%if %{with smp}
%files -n kernel-smp-char-ltmodem
%defattr(644,root,root,755)
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}
/lib/modules/%{_kernel_ver}smp/*/*
%endif
