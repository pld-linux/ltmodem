Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul f�r Lucent-Modems
Summary(pl):	Modu� j�dra dla modem�w Lucent
Name:		ltmodem
Version:	6.00c2
Release:	1.1
License:	GPL
Group:		Base/Kernel
URL:		http://www.physcip.uni-stuttgart.de/heby/ltmodem/
Source0:	http://www.physcip.uni-stuttgart.de/heby/ltmodem/%{name}-%{version}.tar.gz
Patch0:		%{name}-make.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.3.0}
ExclusiveArch:	%{ix86}
ExclusiveOS:	Linux

%description
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -l de
ltmodem ist ein Kernmodul, der unterst�tzt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Ger�t gew�hrt.

%description -l pl
ltmodem jest modu�em j�dra obs�uguj�cym modemy oparte na uk�adach
Lucent. Modemy te udost�pniane s� jako urz�dzenie /dev/ttyLT0.

%package -n kernel-net-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul f�r Lucent-Modems
Summary(pl):	Modu� j�dra dla modem�w Lucent
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	modutils >= 2.4.6-3
Requires:	dev >= 2.7.7-9
Conflicts:	ppp < 2.4.0
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Obsoletes:	ltmodem

%description -n kernel-net-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-net-ltmodem -l de
ltmodem ist ein Kernmodul, der unterst�tzt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Ger�t gew�hrt.

%description -n kernel-net-ltmodem -l pl
ltmodem jest modu�em j�dra obs�uguj�cym modemy oparte na uk�adach
Lucent. Modemy te udost�pniane s� jako urz�dzenie /dev/ttyLT0.

%package -n kernel-smp-net-ltmodem
Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul f�r Lucent-Modems
Summary(pl):	Modu� j�dra dla modem�w Lucent
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	modutils >= 2.4.6-3
Requires:	dev >= 2.7.7-9
Conflicts:	ppp < 2.4.0
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	ltmodem

%description -n kernel-smp-net-ltmodem
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyLT0 device.

%description -n kernel-smp-net-ltmodem -l de
ltmodem ist ein Kernmodul, der unterst�tzt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyLT0-Ger�t gew�hrt.

%description -n kernel-smp-net-ltmodem -l pl
ltmodem jest modu�em j�dra obs�uguj�cym modemy oparte na uk�adach
Lucent. Modemy te udost�pniane s� jako urz�dzenie /dev/ttyLT0.

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

%post -n kernel-net-ltmodem
/sbin/depmod -a

%postun	-n kernel-net-ltmodem
/sbin/depmod -a

%post -n kernel-smp-net-ltmodem
/sbin/depmod -a

%postun	-n kernel-smp-net-ltmodem
/sbin/depmod -a

%files -n kernel-net-ltmodem
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}/*/*
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}

%if 0
%files -n kernel-smp-net-ltmodem
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}smp/*/*
%doc 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}
%endif
