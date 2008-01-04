# NOTE
# - Unusable in PLD Linux as our PHP is compiled with ZTS, while this extension is not
# - Can't find what Free Download means (http://www.zend.com/free_download/list)
%define		php4_version	4.4
%define		php5_version	5.2
Summary:	The Zend Debug Server enabling remote debugging of PHP applications
Summary(pl.UTF-8):	Zend Debug Server pozwalający na zdalne śledzenie aplikacji PHP
Name:		ZendDebugger
Version:	5.2.10
Release:	0.4
License:	Free Download
Group:		Development/Languages/PHP
Source0:	http://downloads.zend.com/pdt/server-debugger/%{name}-%{version}-linux-glibc21-i386.tar.gz
# NoSource0-md5:	d2ee7659c0c8721221696cab5e765936
NoSource:	0
Source1:	http://downloads.zend.com/pdt/server-debugger/%{name}-%{version}-linux-glibc23-x86_64.tar.gz
# NoSource1-md5:	3238904ebd1accd5795a50fb88fc6fff
NoSource:	1
URL:		http://www.zend.com/store/software/zend_studio
BuildRequires:	tar >= 1:1.15.1
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	%{_prefix}/share/Zend
%define		no_install_post_strip		1
%define		no_install_post_chrpath		1
%define		_php4_extensiondir	%{_libdir}/php4
%define		_php5_extensiondir	%{_libdir}/php
%define		_php4_sysconfdir	/etc/php4/conf.d
%define		_php5_sysconfdir	/etc/php/conf.d

%description
The Zend Debug Server enables remote debugging of PHP applications. It
plugs into a PHP server and allows the Zend Development Environment to
control the execution of PHP applications on the server.

The Debug Server is designed be deployed safely on production servers.
It does not affect server performance and features access-list based
security for protecting the server from unauthorized access.

%description -l pl.UTF-8
Zend Debug Server pozwala na zdalne śledzenie aplikacji PHP. Podłącza
się do serwera PHP i pozwala środowisku Zend Development Environment
sterować wykonywaniem aplikacji PHP na serwerze.

Debug server jest zaprojektowany z myślą o bezpiecznym wdrożeniu na
serwerach produkcyjnych. Nie wpływa na wydajność serwera i cechuje się
bezpieczeństwem opartym na listach dostępu.

%package -n php4-%{name}
Summary:	Zend Debugger for PHP 4.x
Summary(pl.UTF-8):	Zend Debugger dla PHP 4.x
Group:		Development/Languages/PHP
Requires:	php4(thread-safety) = 0
Requires:	php4-common < 3:%(awk 'BEGIN{print %{php4_version} + 0.1}')
Requires:	php4-common >= 3:%{php4_version}
Conflicts:	ZendStudioServer <= 5.2.0

%description -n php4-%{name}
The Zend Debug Server enables remote debugging of PHP applications. It
plugs into a PHP server and allows the Zend Development Environment to
control the execution of PHP applications on the server.

The Debug Server is designed be deployed safely on production servers.
It does not affect server performance and features access-list based
security for protecting the server from unauthorized access.

%description -n php4-%{name} -l pl.UTF-8
Zend Debug Server pozwala na zdalne śledzenie aplikacji PHP. Podłącza
się do serwera PHP i pozwala środowisku Zend Development Environment
sterować wykonywaniem aplikacji PHP na serwerze.

Debug server jest zaprojektowany z myślą o bezpiecznym wdrożeniu na
serwerach produkcyjnych. Nie wpływa na wydajność serwera i cechuje się
bezpieczeństwem opartym na listach dostępu.

%package -n php-%{name}
Summary:	Zend Debugger for PHP 5.x
Summary(pl.UTF-8):	Zend Debugger dla PHP 5.x
Group:		Development/Languages/PHP
Requires:	php-common < 4:%(awk 'BEGIN{print %{php5_version} + 0.1}')
Requires:	php-common >= 4:%{php5_version}
Requires:	php5(thread-safety) = 0
Conflicts:	ZendStudioServer <= 5.2.0

%description -n php-%{name}
The Zend Debug Server enables remote debugging of PHP applications. It
plugs into a PHP server and allows the Zend Development Environment to
control the execution of PHP applications on the server.

The Debug Server is designed be deployed safely on production servers.
It does not affect server performance and features access-list based
security for protecting the server from unauthorized access.

%description -n php-%{name} -l pl.UTF-8
Zend Debug Server pozwala na zdalne śledzenie aplikacji PHP. Podłącza
się do serwera PHP i pozwala środowisku Zend Development Environment
sterować wykonywaniem aplikacji PHP na serwerze.

Debug server jest zaprojektowany z myślą o bezpiecznym wdrożeniu na
serwerach produkcyjnych. Nie wpływa na wydajność serwera i cechuje się
bezpieczeństwem opartym na listach dostępu.

%prep
%setup -qcT
%ifarch %{x8664}
tar --strip-components=1 -xzf %{SOURCE1}
%else
tar --strip-components=1 -xzf %{SOURCE0}
%endif

cat > zend.ini <<EOF
[Zend]
zend_debugger.allow_hosts=127.0.0.1
zend_debugger.expose_remotely=always
EOF

cat <<'EOF' > pack4.ini
; %{name} package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_extension=%{_php4_extensiondir}/ZendDebugger.so
EOF

cat <<'EOF' > pack5.ini
; %{name} package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_extension=%{_php5_extensiondir}/ZendDebugger.so
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_php4_extensiondir},%{_php5_extensiondir}}
install %(echo %{php4_version} | tr . _)_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_php4_extensiondir}
install %(echo %{php5_version} | tr . _)_x_comp/ZendDebugger.so $RPM_BUILD_ROOT%{_php5_extensiondir}

install -d $RPM_BUILD_ROOT{%{_php4_sysconfdir},%{_php5_sysconfdir}}
install zend.ini $RPM_BUILD_ROOT%{_php4_sysconfdir}/%{name}.ini
install zend.ini $RPM_BUILD_ROOT%{_php5_sysconfdir}/%{name}.ini
install pack4.ini $RPM_BUILD_ROOT%{_php4_sysconfdir}/%{name}_pack.ini
install pack5.ini $RPM_BUILD_ROOT%{_php5_sysconfdir}/%{name}_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php4-%{name}
if [ "$1" = "0" ]; then
	%php4_webserver_restart
fi

%post -n php4-%{name}
%php4_webserver_restart

%preun -n php-%{name}
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%post -n php-%{name}
%php_webserver_restart

%files -n php4-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_php4_sysconfdir}/%{name}.ini
%config %verify(not md5 mtime size) %{_php4_sysconfdir}/%{name}_pack.ini
%attr(755,root,root) %{_php4_extensiondir}/ZendDebugger.so

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_php5_sysconfdir}/%{name}.ini
%config %verify(not md5 mtime size) %{_php5_sysconfdir}/%{name}_pack.ini
%attr(755,root,root) %{_php5_extensiondir}/ZendDebugger.so
