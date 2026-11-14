param(
    [string]$AuthorName = 'K-Terang',
    [string]$AuthorEmail = 'greatryuhg@gmail.com'
)

$ErrorActionPreference = 'Stop'
$repoPath = $PSScriptRoot
$remoteUrl = 'https://github.com/K-Ternag/moadollHome.git'

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArgs)
    & git -C $repoPath @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Git failed: $($GitArgs -join ' ')"
    }
}

Push-Location -LiteralPath $repoPath
try {
    & python build_site.py
    if ($LASTEXITCODE -ne 0) { throw 'Website generation failed.' }
    & python verify_site.py
    if ($LASTEXITCODE -ne 0) { throw 'Website verification failed.' }

    if (-not (Test-Path -LiteralPath (Join-Path $repoPath '.git'))) {
        Invoke-Git -GitArgs @('init', '-b', 'main')
    }
    $branchName = & git -C $repoPath symbolic-ref --quiet --short HEAD
    if ($LASTEXITCODE -ne 0 -or $branchName -ne 'main') {
        throw 'Expected the local main branch. Review the current branch before publishing.'
    }
    $remotes = @(Invoke-Git -GitArgs @('remote'))
    if ($remotes -notcontains 'origin') {
        Invoke-Git -GitArgs @('remote', 'add', 'origin', $remoteUrl)
    } else {
        $existingRemote = Invoke-Git -GitArgs @('remote', 'get-url', 'origin')
        if ($existingRemote -ne $remoteUrl -and $existingRemote -ne $remoteUrl.Replace('.git', '')) {
            throw "Origin points to another repository: $existingRemote"
        }
    }

    # Read the remote first; never replace unrelated history or force a push.
    $remoteHeads = @(Invoke-Git -GitArgs @('ls-remote', '--heads', 'origin'))
    if ($remoteHeads.Count -gt 0) {
        Invoke-Git -GitArgs @('fetch', 'origin')
        & git -C $repoPath rev-parse --quiet --verify HEAD | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw 'The remote now has commits but this local repository does not. Stop and reconcile the histories before uploading.'
        }
        & git -C $repoPath rev-parse --quiet --verify origin/main | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'The remote has history on another branch. Review it before uploading.' }
        & git -C $repoPath merge-base --is-ancestor origin/main HEAD
        if ($LASTEXITCODE -ne 0) { throw 'Remote main has changes missing locally. Integrate them before uploading.' }
    }

    Invoke-Git -GitArgs @('add', '--all')
    & git -C $repoPath diff --cached --quiet
    $stagedStatus = $LASTEXITCODE
    if ($stagedStatus -eq 1) {
        Invoke-Git -GitArgs @('-c', "user.name=$AuthorName", '-c', "user.email=$AuthorEmail", 'commit', '-m', 'Build bilingual MoaDoll website with support and privacy pages')
    } elseif ($stagedStatus -ne 0) {
        throw 'Unable to inspect staged changes.'
    }
    Invoke-Git -GitArgs @('push', '-u', 'origin', 'main')
    $localHead = Invoke-Git -GitArgs @('rev-parse', 'HEAD')
    $remoteHead = Invoke-Git -GitArgs @('ls-remote', 'origin', 'refs/heads/main')
    if (-not $remoteHead -or (($remoteHead -split '\s+')[0] -ne $localHead)) {
        throw 'Push returned, but remote main could not be verified.'
    }
    Write-Host "Uploaded commit $localHead to $remoteUrl"
} finally {
    Pop-Location
}
