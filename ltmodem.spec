Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	6.00c2
Release:	1.2
License:	GPL
Group:		Base/Kernel
Source0:	http://www.physcip.uni-stuttgart.de/heby/ltmodem/%{name}-%{version}.tar.gz
Patch0:		%{name}-make.patch
URL:		http://www.physcip.uni-stuttgart.de/heby/ltmodem/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.3.0}
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
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
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
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
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
%patch0 -p1

%build
cd source
%{__autoconf}

CFLAGS="%{rpmcflags} -I%{_kernelsrcdir}/include"
%configure \
	--with-force=yes \
	--with-kernel=%{_kernelsrcdir}
%{__make}
mv lt_*.o lt*.a ..

%if 0
CFLAGS="$CFLAGS -D__KERNEL_SMP=1"
%configure \
	--with-force=yes \
	--with-kernel=%{_kernelsrcdir}
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -dD $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
cp -f lt_*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%if 0
cp -f source/lt_*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif

rm -rf DOCs/Installers

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-char-ltmodem
/sbin/depmod -a

%postun	-n kernel-char-ltmodem
/sbin/depmod -a

%post -n kernel-smp-char-ltmodem
/sbin/depmod -a

%postun	-n kernel-smp-char-ltmodem
/sbin/depmod -a

%files -n kernel-char-ltmodem
%defattr(644,root,root,755)
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}
/lib/modules/%{_kernel_ver}/*/*

%if 0
%files -n kernel-smp-char-ltmodem
%defattr(644,root,root,755)
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}
/lib/modules/%{_kernel_ver}smp/*/*
%endif
