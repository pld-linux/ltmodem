%define ver_major 5
%define ver_minor 78

Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	%{ver_major}.%{ver_minor}
Release:	1
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://walbran.org/sean/linux/stodolsk/i56lvp%{ver_major}%{ver_minor}.zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	unzip
Prereq:		modutils >= 2.3.18-2
ExclusiveArch:	%{ix86}
ExclusiveOS:	Linux

%define		_kernel_ver	%(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)

%description
ltmodem is a kernel module supporting Lucent-chip-based modems. These
modems are made available as the /dev/ttyS14 device.

%description -l de
ltmodem ist ein Kernmodul, der unterstützt Lucent-Chip-basierte
Modems. Diese Modems werden als das /dev/ttyS14-Gerät gewährt.

%description -l pl
ltmodem jest modu³em j±dra obs³uguj±cym modemy oparte na uk³adach
Lucent. Modemy te udostêpniane s± jako urz±dzenie /dev/ttyS14.

%prep
%setup -qcT
unzip %{SOURCE0}

%build
# forget the Makefile. It sucks.
gcc -D__KERNEL__ -DMODULE $RPM_OPT_FLAGS -c *.c
ld -r -o lt.o *.o

%install
rm -rf $RPM_BUILD_ROOT
install -D lt.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/net/ltmodem.o
install -d $RPM_BUILD_ROOT/dev
mknod $RPM_BUILD_ROOT/dev/ttyS14 c 62 78

%files
%defattr(644,root,root,755)
%attr(664,root,ttyS) /dev/*
%attr(600,root,root) /lib/modules/*/*/*

%post
depmod -a

%postun
depmod -a

%clean
rm -rf $RPM_BUILD_ROOT
