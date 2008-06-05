#Module-Specific definitions
%define apache_version 2.2.0
%define mod_name mod_authz_unixgroup
%define mod_conf A57_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache Unix Group Access Control Modules
Name:		apache-%{mod_name}
Version:	1.0.0
Release:	%mkrel 5
Group:		System/Servers
License:	Apache License
URL:		http://unixpapa.com/mod_authz_unixgroup/
Source0:	http://www.unixpapa.com/software/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires:	pwauth
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod_Authz_Unixgroup is a unix group access control modules for Apache 2.1 and
later. If you are having users authenticate with real Unix login ID over the
net, using something like my mod_authnz_external / pwauth combination, and you
want to do access control based on unix group membership, then
mod_authz_unixgroup is exactly what you need.

%prep

%setup -q -n %{mod_name}-%{version}

chmod 644 CHANGES INSTALL README

rm -rf .libs

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


