Name:           tang
Version:        8
Release:        3%{?dist}
Summary:        Network Presence Binding Daemon

License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  git-core
BuildRequires:  jose >= 8
BuildRequires:  libjose-devel >= 8
BuildRequires:  libjose-zlib-devel >= 8
BuildRequires:  libjose-openssl-devel >= 8

BuildRequires:  http-parser-devel >= 2.7.1-3
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig

BuildRequires:  systemd
BuildRequires:  curl

BuildRequires:  asciidoc
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  sed

%{?systemd_requires}
Requires:       coreutils
Requires:       jose >= 8
Requires:       grep
Requires:       sed

Requires(pre):  shadow-utils

%description
Tang is a small daemon for binding data to the presence of a third party.

%prep
%autosetup -S git

%build
%meson
%meson_build

%install
%meson_install
echo "User=%{name}" >> $RPM_BUILD_ROOT/%{_unitdir}/%{name}d@.service
%{__mkdir_p} $RPM_BUILD_ROOT/%{_localstatedir}/db/%{name}

%check
%meson_test

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/cache/%{name} -s /sbin/nologin \
    -c "Tang Network Presence Daemon user" %{name}
exit 0

%post
%systemd_post %{name}d.socket

%preun
%systemd_preun %{name}d.socket

%postun
%systemd_postun_with_restart %{name}d.socket

%files
%license COPYING
%attr(0700, %{name}, %{name}) %{_localstatedir}/db/%{name}
%{_unitdir}/%{name}d@.service
%{_unitdir}/%{name}d.socket
%{_libexecdir}/%{name}d-keygen
%{_libexecdir}/%{name}d
%{_mandir}/man8/tang.8*
%{_bindir}/%{name}-show-keys
%{_mandir}/man1/tang-show-keys.1*
