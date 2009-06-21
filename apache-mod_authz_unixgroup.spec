#Module-Specific definitions
%define apache_version 2.2.0
%define mod_name mod_authz_unixgroup
%define mod_conf A57_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache Unix Group Access Control Modules
Name:		apache-%{mod_name}
Version:	1.0.2
Release:	%mkrel 1
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/mod-auth-external/wiki/ModAuthzUnixGroup
Source0:	http://mod-auth-external.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
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

cp %{SOURCE1} %{mod_conf}


%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


