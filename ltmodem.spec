Summary:	Kernel module for Lucent modems
Summary(de):	Kernmodul für Lucent-Modems
Summary(pl):	Modu³ j±dra dla modemów Lucent
Name:		ltmodem
Version:	5.78e
Release:	1
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://www.tux.org/pub/dclug/marvin/%{name}-%{version}.tar.gz
Patch0:		%{name}-make.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	unzip
Prereq:		modutils >= 2.3.18-2
Requires:	dev >= 2.7.7-9
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
%setup -q
tar -xzC.. -f %{name}-%{version}.tar.gz
%patch0 -p1

%build
CFLAGS="${CFLAGS:-%optflags}%{?debug: -g -O0}" \
CC=gcc KVERSION=%{_kernel_ver} make

%install
rm -rf $RPM_BUILD_ROOT
install -D ltmodem.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ltmodem.o
gzip -9nf [CU1]*

%files
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/*/*/*
%doc C*
%doc U*
%doc 1*

%post
depmod -a

%postun
depmod -a

%clean
rm -rf $RPM_BUILD_ROOT
