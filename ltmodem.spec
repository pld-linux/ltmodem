%define		_kernel_ver %(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		smpstr	%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp	%{?_with_smp:1}%{!?_with_smp:0}

Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	5.99b
Release:	2@%{_kernel_ver}%{smpstr}
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
URL:		http://www.heby.de/ltmodem/
Source0:	http://www.tux.org/pub/dclug/marvin/%{name}-%{version}.tar.gz
Patch0:		%{name}-make.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
BuildConflicts:	kernel < 2.3.0
Prereq:		modutils >= 2.4.6-3
Requires:	dev >= 2.7.7-9
Conflicts:	ppp < 2.4.0
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
BuildConflicts:	kernel-headers < 2.4.0
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

%prep
%setup -q
tar xzf source.tar.gz
%patch0 -p1

%build
cd source
autoconf
%if %{smp}
CFLAGS="%{rpmcflags} -D__KERNEL_SMP=1"
%endif
%configure \
	--with-force=yes \
	--with-kernel=/usr/src/linux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -dD $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -m644 source/lt_*.o $RPM_BUILD_ROOT/lib/modules/*/misc

gzip -9nf 1ST-READ DOCs/* source/{CHANGELOG,UPDATES-BUGS}

%files
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/*/*
%doc 1ST-READ*
%doc DOCs/*
%doc source/*.gz

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%clean
rm -rf $RPM_BUILD_ROOT
