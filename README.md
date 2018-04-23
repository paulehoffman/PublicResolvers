This site has an informal list of public resolvers for DNS.
There are many definitions of what a “public resolver” is.
This list is based on the following rules:

* There must be a web site managed by the provider that gives
the IP addresses of the public resolver

* There must be no sign-up required for using the resolver

* The resolver can change the answers for queries such as
to provide some sort of “protection”, but it must not
give positive answers for names that do not exist in the
public DNS (such as adding new TLDs)

* The resolver must support either normal DNS resolution
over port 53 and/or DNS-over-TLS (RFC 7858) over port 853.
DNS-over-HTTPS (also known as DOH) will be added to the
list when DOH is standardized.

Note that what is described here is public resolvers,
not “open resolvers”. The latter generally refers to resolvers
that are available but may not be available intentionally.
The primary difference could be the requirement for a web site
listing the addresses. For example, many people call
4.2.2.1 a public resolver run by Level3, although there
is no web page run by Level3 indicating support for
the resolver.

Changes and additions to this list can be made by opening
issues or sending pull requests. The list is maintained
by [Paul Hoffman](phoffman@proper.com).

Note that there are many other lists of public resolvers 
and open resolvers. Those lists usually have different
rules for inclusion than this one does.

If you're interested in public resolvers that offer
privacy services, [this page]
(https://dnsprivacy.org/wiki/display/DP/DNS+Privacy+Test+Servers)
is kept up to date by folks active in the DNS community.

