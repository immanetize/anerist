from pkgdb2client import PkgDB
import git
import hashlib
import os
import shutil
import errno
import sys

class PublicanHelpers():
    def valid_formats(self):
        valid_formats = [
                "drupal-book",
                "eclipse",
                "epub",
                "html",
                "html-desktop",
                "html-single",
                "man",
                "pdf",
                "txt",
                "xml"
                ]
        return valid_formats
    def valid_langs(self):
        language_list = [
            "ar-sa",
            "as-in",
            "ast-es",
            "bn-in",
            "bs-ba",
            "bg-bg",
            "ca-es",
            "zh-cn",
            "zh-hk",
            "zh-tw",
            "cs-CZ",
            "da-DK",
            "fi-FI",
            "fr-FR",
            "de-DE",
            "el-GR",
            "gu-IN",
            "he-IL",
            "hi-IN",
            "hr-HR",
            "hu-HU",
            "id-ID",
            "ia",
            "is-IS",
            "it-IT",
            "ja-JP",
            "kn-IN",
            "ko-KR",
            "lv-LT",
            "lv-LV",
            "ml-IN",
            "mr-IN",
            "nb-NO",
            "nl-NL",
            "or-IN",
            "pa-IN",
            "fa-IR",
            "pl-PL",
            "pt-PT",
            "pt-BR",
            "ro-RO",
            "ru-RU",
            "sr-RS",
            "sr-Latn-RS",
            "si-LK",
            "sk-SK",
            "es-ES",
            "sv-SE",
            "ta-IN",
            "te-IN",
            "uk-UA",
            "de-CH",
            "th-TH"
            ]
        return language_list

class FedoraHelpers():
    def guide_git_url(self, guide):
        anon_url = "https://git.fedorahosted.org/git/docs/%s.git" % guide
        # ssh_url = "ssh://git.fedorahosted.org/git/docs/%s.git" % guide
        ssh_url = "ssh://buildbot@lemuria.home.randomuser.org:/srv/projects/docs/guides/%s" % guide
        return anon_url, ssh_url
    def get_remote_branches(self, guide=None, remote=None):
        from git import Repo
        if guide is None and remote is None:
            print("""
             remote must be provided.  You can provide a guide name, and the function
             will generate a fedorahosted url, but at least one of 'guide' or 'remote'
             must be passed.
             """)
            sys.exit(1)
        elif guide and not remote:
            remote, garbage = self.guide_git_url(guide)
        elif not guide and remote:
            # try to parse out what the local directory name would be
            guide = self._reponame_extractor(remote)
        # this needs to be smarter    
        repodir = "%s/%s" % (os.getcwd(), guide)
        if not os.path.exists(repodir):
            repo_hash = hashlib.md5()
            repo_hash.update(remote)
            repodir = '/tmp/anerist/%s-fetcher' % repo_hash.hexdigest()
            if os.path.exists(repodir):
                try:
                    shutil.rmtree(repodir)
                except OSError:
                    print("unable to clean up temporary directory for %s, %s" % (guide, repodir))
            self.mkdir_p(repodir)
            repo = Repo.init(repodir)
            origin = repo.create_remote('origin', remote)
            cleanup = True
        else:
            cleanup = False
            repo = Repo(repodir)
            origin = repo.remote('origin')
            try:
                u = origin.url
            except:
                origin = repo.create_remote('origin', remote)
            assert repo.bare
        assert origin == repo.remotes.origin == repo.remotes['origin']
        git = repo.git
        remote_heads = git.ls_remote("--heads").split()
        remote_heads = [x for x in remote_heads if x.startswith('refs/heads/f')]
        for index, head in enumerate(remote_heads):
            remote_heads[index] = head.replace('refs/heads/', '')
        published_branches = self.release_tracker()
        published_heads = list(set(remote_heads).intersection(set(published_branches)))
        if cleanup: 
            shutil.rmtree(repodir)
        published_heads.append('master')
        return published_heads

    def mkdir_p(self, path):
        # thanks tzot, http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
        try:
                os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
    def _reponame_extractor(self, remote):
        reponame = os.path.basename(remote)
        if reponame.endswith('.git'):
            reponame = reponame[:-len('.git')]
        return reponame
    
    def release_tracker(self):
        release_checker = PkgDB()
        published_releases = []
        a = release_checker.get_collections('f*', clt_status=["Active", "EOL", "Under Development"])
        eol_releases = []
        for release in a['collections']:
            if release['status'] == "Active" or release["status"] == "Under Development":
                published_releases.append(release['branchname'])
            elif release['status'] == "EOL":
                eol_releases.append(int(release['version']))
        for release in a['collections']:
            if int(release['version']) == max(eol_releases):
                published_releases.append(release['branchname'])
        return published_releases
    def published_publican_guides(self):
        all_guides = set(self.all_publican_guides())
        old_guides = set(self.deprecated_publican_guides())
        published_guides = list(all_guides.difference(old_guides))
        return published_guides
    def all_publican_guides(self):
        guide_list = [
                "user-guide",
                "openssh-guide",
                "securityguide",
                "software-collections-guide",
                "software-management-guide",
                "systemtap-beginners-guide",
                "virtualization-security-guide",
                "robotics-guide",
                "technical-notes",
                "packagers-guide",
                "fedora-server-guide",
                "multiboot-guide",
                "cloud-guide",
                "anaconda-addon-development-guide",
                "jargon-buster",
                "elections-guide",
                "selinux-user-guide",
                "uefi-secure-boot-guide",
                "power-management-guide",
                "freeipa-guide",
                "install-guide",
                "secure-ruby-development-guide",
                "writers-style-guide",
                "virtualization-guide",
                "system-administrators-reference-guide",
                "fedora-cookbook",
                "wirelessguide",
                "release-notes",
                "networking-guide",
                "installation-quick-start-guide",
                "resource-management-guide",
                "readme-burning-isos",
                "respin-guide",
                "documentation-guide",
                "accessibility-guide",
                "musicians-guide",
                "storage-administration-guide",
                "rpm-guide",
                "amateur-radio-guide",
                "docs-beginner",
                "docsite-publican",
                "translation-quick-start-guide",
                "virtualization-administration-guide",
                "system-administrators-guide",
                "virtualization-deployment-guide",
                "ARM-getting-started-guide",
                "readme-live-image",
                "deployment-guide",
                "virtualization-getting-started-guide",
                "selinux-guide",
                "virtualization-deployment-and-administration-guide",
                "firewall-guide"
                ]
        return guide_list
    def deprecated_publican_guides(self):
        guide_list = [
            "user-guide",
            "docsite-publican",
            "openssh-guide",
            "software-collections-guide",
            "software-management-guide",
            "systemtap-beginners-guide",
            "virtualization-security-guide",
            "robotics-guide",
            "cloud-guide",
            "jargon-buster",
            "freeipa-guide",
            "writers-style-guide",
            "virtualization-guide",
            "system-administrators-reference-guide",
            "wirelessguide",
            "installation-quick-start-guide",
            "resource-management-guide",
            "readme-burning-isos",
            "respin-guide",
            "musicians-guide",
            "amateur-radio-guide",
            "translation-quick-start-guide",
            "virtualization-administration-guide",
            "virtualization-deployment-guide",
            "ARM-getting-started-guide",
            "readme-live-image",
            "deployment-guide",
            "virtualization-deployment-and-administration-guide",
            "selinux-user-guide"
            ]
        return guide_list
