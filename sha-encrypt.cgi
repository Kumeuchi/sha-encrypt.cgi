#!/usr/bin/perl

#SHA-256 encrypt

use strict;
use Digest::SHA qw(sha1_hex sha256_hex sha512_hex);
use utf8;
use CGI;
use Encode;
binmode STDOUT, ':utf8';

# encrypt / decrypt functions.
sub encrypt_sha1{
	my($plain, $salt, $includeSalt) = @_;
	if($includeSalt == 1){
		return $salt . sha1_hex($salt, $plain);
	}
	else{
		return sha1_hex($salt, $plain);
	}
}

sub encrypt_sha256{
	my($plain, $salt, $includeSalt) = @_;
	if($includeSalt == 1){
		return $salt . sha256_hex($salt, $plain);
	}
	else{
		return sha256_hex($salt, $plain);
	}
}

sub encrypt_sha512{
	my($plain, $salt, $includeSalt) = @_;
	if($includeSalt == 1){
		return $salt . sha512_hex($salt, $plain);
	}
	else{
		return sha512_hex($salt, $plain);
	}
}

# 初期化
my $q = new CGI;
my $plainPwd = "";
my $salt = "";
my $bIncludeSalt = 0;
my $errMsg = "";
my $submit = "";
my $plainTextErr = 'class = "ok" ';
my $saltErr = 'class = "ok" ';

# POSTメソッドの値を取る
if($q->request_method() eq 'POST'){
	$plainPwd = $q->param('pwd');
	$salt = $q->param('salt');
	$bIncludeSalt = $q->param('includeSalt');
	$submit = $q->param('submit');
	
	# 入力内容チェック
	if($plainPwd eq ""){
		$plainTextErr = 'class = "ng" ';
		$errMsg .= "<li>変換する文字列を入力してください。$!</li>";
	}
	elsif($plainPwd !~ /^[0-9a-zA-Z._-]+$/){
		$plainPwd = $q->escapeHTML($plainPwd);
		$plainTextErr = 'class = "ng" ';
		$errMsg .= "<li>変換する文字列に不正な文字があります。$!</li>";
	}
	if(($salt ne "") && ($salt !~ /^[0-9a-zA-Z]+$/)){
		$salt = $q->escapeHTML($salt);
		$saltErr = 'class = "ng" ';
		$errMsg .= "<li>saltの文字列に不正な文字があります。$!</li>";
	}
}
my $inputPwd = "<input id = \"inputPwd\" type = \"text\" name = \"pwd\" value = \"${plainPwd}\" size = \"60\" ${plainTextErr}/>";
my $inputSalt = "<input id = \"inputSalt\" type = \"text\" name = \"salt\" value = \"$salt\" ${saltErr}/>";
my $includeSalt = "<input id  = \"includeSalt\" type = \"checkbox\" name = \"includeSalt\" value = \"1\" ";
if($bIncludeSalt == 1){
	$includeSalt .= "checked />";
}
else{
	$includeSalt .= "/>";
}

my $encPwd = encrypt_sha1($plainPwd, $salt, $bIncludeSalt);
my $encPwd256 = encrypt_sha256($plainPwd, $salt, $bIncludeSalt);
my $encPwd512 = encrypt_sha512($plainPwd, $salt, $bIncludeSalt);

# html 書き出し
print <<EOM;
Content-type: text/html

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
		"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
<head>
<meta http-equiv = "Content-Type" content = "text/html; charset = utf-8" />
<title>SHA-1/SHA-256/SHA-512暗号化(ハッシュ化)ツール</title>
<meta name = "Author" content = "Kumeuchi Akira" />
<meta name = "keywords" content = "SHA,SHA-1,SHA-256,SHA-512,SHA1,SHA256,SHA512,暗号,暗号化,暗号化ツール,暗号生成,暗号化生成,ハッシュ化,ハッシュ化ツール,ハッシュ作成">
<meta http-equiv = "Content-Style-Type" content = "text/css" />
<link href = "../../styles/styles.css" rel = "stylesheet" type = "text/css" media = "screen,tv" />
<style type = "text/css">
th{font-weight: normal; text-align: right; padding-right: 8px;}
.ok{background-color: #ffffff; height: 1rem;}
.ng{background-color: #ffcccc; height: 1rem;}
input#inputPwd{height: 1rem;}
input#inputSalt{height: 1rem;}
input#includeSalt{width: 1rem; height: 1rem;}
input#submit{width: 4rem; height: 1.5rem; font-size: 1.0rem;}
blockquote{
	color: #473624;
	background-color: #fffaf8;
	border: 1px solid #b12e05;
	padding: 4px 12px 12px 12px;
	margin: 0px 0px 12px 0px;
}
code,tt{
	font-family: Consolas, Menio, "Liberation Mono", Courier, monospace, "メイリオ";
	line-height: 1em;
}

</style>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-3521121-2', 'auto');
  ga('send', 'pageview');

</script>
<script type = "text/javascript" src = "../../gadgets/jquery-3.3.1.min.js"></script>
</head>
<body>
<div id = "container">

<div id = "header">
<h1><a href = "../../">bass-world.net</a></h1>
<h2>SHA-1/SHA-256/SHA-512暗号化(ハッシュ化)ツール</h2>
</div>

<div id = "main">

<div class = "article">
<h2><a name = "sha" id = "sha">SHA-1/SHA-256/SHA-512暗号化(ハッシュ化)ツール</a></h2>
<p>暗号化したい文字列を入力して「変換」ボタンを押すと、SHA-1/SHA-256/SHA-512暗号(ハッシュ)コードを生成します。</p>
<form action = "./sha-encrypt.cgi" method = "post">
<table>
	<tr>
		<th>変換する文字列</th>
EOM
$inputPwd = Encode::decode('UTF-8', $inputPwd);
print("<td>$inputPwd</td>");
print <<EOM;
	</tr>
	<tr>
		<th>salt</th>
EOM
$inputSalt = Encode::decode('UTF-8', $inputSalt);
print("<td>$inputSalt</td>");
print <<EOM;
	</tr>
	<tr>
		<th>saltを先頭に付ける</th>
		<td>$includeSalt</td>
	</tr>
</table>
<p><input type = "submit" id = "submit" name = "submit" value = "変換" style = "margin-bottom:24px;height: 1.8rem;" /></p>
</form>
EOM

if(($errMsg eq '') and (Encode::decode('UTF-8', $submit) eq '変換')){
	print <<EOM;
<ul>
<li>変換前文字列 - 「$plainPwd」
<li>salt - 「$salt」
<li>SHA-1暗号化した文字列<br /><input id = "sha1" type = "text" name = "sha1" value = "${encPwd}" size = "100" onclick="this.select(0,this.value.length)" /></li>
<li>SHA-256暗号化した文字列<br /><input id = "sha256" type = "text" name = "sha256" value = "${encPwd256}" size = "100" onclick="this.select(0,this.value.length)" /></li>
<li>SHA-512暗号化した文字列<br /><input id = "sha512" type = "text" name = "sha512" value = "${encPwd512}" size = "100" onclick="this.select(0,this.value.length)" /></li>
</ul>
EOM
}
else{
print "<ul>$errMsg</ul>\n";
}
print <<EOM;
<h4>変更履歴</h4>
<ul>
<li>16 Feb 2017 - XSS脆弱性に対応しました。</li>
<li>14 Feb 2017 - コードを半分ぐらい書き直しました。</li>
<li>11 Feb 2017 - XSS脆弱性に対応しました。</li>
<li>9 Feb 2017 - saltを暗号化文字列の先頭に付けるか選択できるようにしました。</li>
<li>7 Feb 2017 - テキストボックスをクリックすると全選択するようにしました。</li>
<li>6 Feb 2017 - SHA-512に対応しました。</li>
</ul>
<p>
不具合・ご意見などがありましたら、<a href = "mailto:kumeuchi&#64;gmail.com">kumeuchi&#64;gmail.com</a>までメールください。
</p>
EOM
print <<'EOM';
<h2>暗号化(ハッシュ化)の方法(Perl)</h2>
<blockquote><code><pre>use Digest::SHA qw(sha1_hex sha256_hex sha512_hex);

sub encrypt_sha512{
  my($plain, $salt, $includeSalt) = @_;        # 暗号化する文字列, salt, saltを結果に付加するか
  if($includeSalt == 1){
    return $salt . sha512_hex($salt, $plain);  # 暗号化関数の呼び出し
  }
  else{
    return sha512_hex($salt, $plain);          # 暗号化関数の呼び出し
  }
}</pre></code></blockquote>
EOM
print <<'EOM';
<h2>復号化の方法 - キーを暗号化して比較する (Perl)</h2>
<blockquote><code><pre>use Digest::SHA qw(sha1_hex sha256_hex sha512_hex);

sub decrypt{
  my ($crypt, $plain) = @_;                              # 保存されてある暗号化したパスワード, 入力されたパスワード
  return $crypt eq (sha512_hex($salt . $plain)) ? 1 : 0; # 暗号化関数の呼び出し
}</pre></code></blockquote>
EOM
print <<EOM;
<p>
<a href="https://px.a8.net/svt/ejp?a8mat=2HUPZF+7R32Q+2KX0+1HQ5MP" target="_blank" rel="nofollow">
<img border="0" width="468" height="60" alt="" src="https://www26.a8.net/svt/bgt?aid=150919179013&wid=021&eno=01&mid=s00000012042009024000&mc=1"></a>
<img border="0" width="1" height="1" src="https://www19.a8.net/0.gif?a8mat=2HUPZF+7R32Q+2KX0+1HQ5MP" alt="">
</p>
<p>
<a href="https://px.a8.net/svt/ejp?a8mat=2TC8BV+FXYBDE+2KX0+1ZIDGX" target="_blank" rel="nofollow">
<img border="0" width="468" height="60" alt="" src="https://www27.a8.net/svt/bgt?aid=170211883964&wid=021&eno=01&mid=s00000012042012011000&mc=1"></a>
<img border="0" width="1" height="1" src="https://www13.a8.net/0.gif?a8mat=2TC8BV+FXYBDE+2KX0+1ZIDGX" alt="">
</p>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-9815219419561283"
     data-ad-slot="6258040412"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div><!-- content -->

<p class = "nav">| <a href = "../../gadgets">gadgets</a> | <a href = "../../">home</a> |</p>

</div><!-- main -->

<div id = "menu">
<div id = "sidebar">
<h2>navigation</h2>
<ul>
	<li><a href = "../../gadgets/">gadgets</a></li>
	<li><a href = "../../">home</a></li>
</ul>
</div><!-- sidebar -->
</div><!-- menu -->

</div><!-- container -->
</body>
</html>
EOM
